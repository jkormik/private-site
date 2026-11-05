from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db, bcrypt
from blog.models import BlogPost
from admin.forms import BlogPostForm, LoginForm
from dotenv import load_dotenv
import os


# Search for a .env file and load it into application environment variables
load_dotenv()

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- Simple Auth Configuration ---
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD") # Now expects a hashed password

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
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Verify password using bcrypt instance from extensions
        if username == ADMIN_USERNAME and bcrypt.check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
            
    return render_template('admin/login.html', form=form)

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
    Create a new blog post using a validated form.
    """
    form = BlogPostForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        is_published = form.is_published.data
        
        slug = generate_slug(title)
        
        # Better collision handling: incremental numbering
        counter = 1
        original_slug = slug
        while BlogPost.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1

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
        except Exception:
            db.session.rollback()
            flash('A system error occurred while saving the post.', 'danger')

    return render_template('admin/create_post.html', form=form, post=None, is_edit=False)

@admin_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """
    Edit an existing blog post using a validated form.
    """
    try:
        post = BlogPost.query.get_or_404(post_id)
    except Exception as e:
        flash(f"Could not find post with ID {post_id}", "danger")
        return redirect(url_for('admin.dashboard'))
    
    form = BlogPostForm(obj=post) # Pre-populate form with post data
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        is_published = form.is_published.data
        
        # Slug logic: only change if title changed or manual slug provided
        new_slug = form.slug.data if form.slug.data else generate_slug(title)
        
        if new_slug != post.slug:
            counter = 1
            original_slug = new_slug
            while BlogPost.query.filter(BlogPost.slug == new_slug, BlogPost.id != post.id).first():
                new_slug = f"{original_slug}-{counter}"
                counter += 1
            post.slug = new_slug
            
        post.title = title
        post.content = content
        post.is_published = is_published
        
        try:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception:
            db.session.rollback()
            flash('A system error occurred while updating the post.', 'danger')
            
    return render_template('admin/create_post.html', form=form, post=post, is_edit=True)

@admin_bp.route('/delete/<int:post_id>', methods=['POST'])
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
    except Exception:
        db.session.rollback()
        flash('A system error occurred while deleting the post.', 'danger')
    
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
