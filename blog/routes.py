from flask import Blueprint, render_template, abort, request
from extensions import db
from blog.models import BlogPost
import markdown
import bleach

# Create the blog blueprint for modular routing
blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    """
    Blog Index Page
    Fetches all published blog posts and displays them.
    Supports filtering by tag.
    """
    tag_filter = request.args.get('tag')
    try:
        query = BlogPost.query.filter_by(is_published=True)
        if tag_filter:
            query = query.filter_by(tag=tag_filter)
        
        posts = query.order_by(BlogPost.date_posted.desc()).all()
        
        # Get all unique tags for the tag cloud
        all_tags = db.session.query(BlogPost.tag).filter(BlogPost.tag.isnot(None)).distinct().all()
        tags = [t[0] for t in all_tags]
        
        return render_template('blog/index.html', posts=posts, tags=tags, current_tag=tag_filter)
    except Exception as e:
        # Log error here in a real app
        abort(500)

@blog_bp.route('/<string:slug>')
def post(slug):
    """
    Single Post View
    Fetches a single blog post by its unique slug and renders its sanitized markdown content.
    """
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    # 1. Convert markdown content to HTML
    raw_html = markdown.markdown(post.content, extensions=['fenced_code', 'tables'])
    
    # 2. Sanitize HTML to prevent Stored XSS
    # We allow a safe set of tags and attributes
    allowed_tags = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'strong', 
        'ul', 'ol', 'li', 'p', 'br', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
        'hr', 'pre', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'div'
    ]
    allowed_attrs = {
        'a': ['href', 'title', 'target'],
        'abbr': ['title'],
        'span': ['class'],
        'div': ['class'],
    }
    
    content_html = bleach.clean(raw_html, tags=allowed_tags, attributes=allowed_attrs)
    
    return render_template('blog/post.html', post=post, content_html=content_html)
