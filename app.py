from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from blog.routes import blog_bp

# Initialize Flask Application
app = Flask(__name__)

# --- Configuration ---
# Using SQLite for local development as per PLAN.md
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-this-in-production'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# --- Blueprints ---
# Register the blog blueprint. 
# This makes the routes in blog/routes.py available under /blog
app.register_blueprint(blog_bp, url_prefix='/blog')

# --- Routes ---

@app.route('/')
def home():
    """
    Homepage
    Renders the home template for Phase 1.
    """
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
