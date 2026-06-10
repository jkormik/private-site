from flask import Blueprint, render_template

# Create the blog blueprint for modular routing
blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    """
    Blog Index Page
    Renders the blog index template for Phase 1.
    """
    return render_template('blog/index.html')
