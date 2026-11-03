from flask import Flask, render_template
from extensions import db
from blog.routes import blog_bp
from admin.routes import admin_bp
import blog.models # Ensure models are registered with SQLAlchemy
from dotenv import load_dotenv
import os
from data import RESUME_DATA

# Search for a .env file and load it into application environment variables
load_dotenv()

# Initialize Flask Application
app = Flask(__name__)

# --- Configuration ---
# Using SQLite for local development as per PLAN.md
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///site.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret-key-change-this-in-production")

# Initialize SQLAlchemy
db.init_app(app)

with app.app_context():
    db.create_all()

# --- Blueprints ---
app.register_blueprint(blog_bp, url_prefix='/blog')
app.register_blueprint(admin_bp)

# --- Routes ---
@app.route('/')
def home():
    """
    Homepage
    Renders the resume template with professional data.
    """
    return render_template('resume.html', data=RESUME_DATA)

if __name__ == '__main__':
    app.run(debug=True)
