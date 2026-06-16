from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from blog.models import BlogPost

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- Simple Auth Configuration ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123" 

def login_required(f):
    """
    Custom decorator to restrict access to admin routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Admin Login Page.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
            
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def dashboard():
    """
    Admin Dashboard.
    Lists all posts for management.
    """
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('admin/dashboard.html', posts=posts)

@admin_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_post():
    """
    Create a new blog post.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        is_published = 'is_published' in request.form
        
        slug = generate_slug(title)
        
        # Check if slug already exists
        existing = BlogPost.query.filter_by(slug=slug).first()
        if existing:
            import time
            slug = f"{slug}-{int(time.time())}"

        new_post = BlogPost(
            title=title, 
            slug=slug, 
            content=content, 
            is_published=is_published
        )
        
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving post: {str(e)}', 'danger')

    return render_template('admin/create_post.html')

@admin_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """
    Edit an existing blog post.
    """
    post = BlogPost.query.get_or_404(post_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        is_published = 'is_published' in request.form
        
        # Regenerate slug if title changed
        new_slug = generate_slug(title)
        if new_slug != post.slug:
            # Check for collision
            existing = BlogPost.query.filter_by(slug=new_slug).first()
            if existing:
                import time
                new_slug = f"{new_slug}-{int(time.time())}"
            post.slug = new_slug
            
        post.title = title
        post.content = content
        post.is_published = is_published
        
        try:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating post: {str(e)}', 'danger')
            
    return render_template('admin/create_post.html', post=post, is_edit=True)

@admin_bp.route('/delete/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    """
    Deletes a blog post by its ID.
    """
    post = BlogPost.query.get_or_404(post_id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash(f'Post "{post.title}" has been deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting post: {str(e)}', 'danger')
    
    return redirect(url_for('admin.dashboard'))

def generate_slug(text):
    """
    Converts a title into a URL-friendly slug.
    """
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text
