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
