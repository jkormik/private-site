from flask import Blueprint, render_template, abort
from extensions import db
from blog.models import BlogPost

# Create the blog blueprint for modular routing
blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    """
    Blog Index Page
    Fetches all published blog posts and displays them.
    """
    try:
        # Query posts that are marked as published, ordered by date (newest first)
        posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.date_posted.desc()).all()
        return render_template('blog/index.html', posts=posts)
    except Exception as e:
        # Log error here in a real app
        abort(500)

@blog_bp.route('/<string:slug>')
def post(slug):
    """
    Single Post View
    Fetches a single blog post by its unique slug.
    """
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('blog/post.html', post=post)
