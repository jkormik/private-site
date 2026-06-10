from datetime import datetime
from extensions import db


class BlogPost(db.Model):
    """
    Model for Blog Posts
    """
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False) # URL-friendly version of title
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<BlogPost {self.title}>'
