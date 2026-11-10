from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from extensions import db, bcrypt
from blog.routes import blog_bp
from admin.routes import admin_bp
import blog.models # Ensure models are registered with SQLAlchemy
from dotenv import load_dotenv
import os
import markdown
from data import RESUME_DATA
from datetime import datetime

# Search for a .env file and load it into application environment variables
load_dotenv()

# Initialize Flask Application
app = Flask(__name__)

# --- Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///site.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret-key-change-this-in-production")

# --- Security Hardening ---
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False, # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE='Lax',
)

# Initialize Extensions
db.init_app(app)
bcrypt.init_app(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

# Render markdown to HTML in templates: {{ text | markdown | striptags }}
app.jinja_env.filters['markdown'] = lambda text: markdown.markdown(text, extensions=['fenced_code', 'tables'])

def format_date_ru(date):
    if not date:
        return ""
    months = {
        1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
        5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
        9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }
    return f"{months[date.month]} {date.day}, {date.year}"

app.jinja_env.filters['date_ru'] = format_date_ru

def calculate_reading_time(text):
    if not text:
        return 0
    # Средняя скорость чтения человека ~200 слов в минуту
    words_per_minute = 200
    word_count = len(text.split())
    reading_time = max(1, round(word_count / words_per_minute))
    return reading_time

app.jinja_env.filters['reading_time'] = calculate_reading_time

# --- Blueprints ---
app.register_blueprint(blog_bp, url_prefix='/blog')
app.register_blueprint(admin_bp)

# Create tables on first run so a fresh clone works (idempotent)
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route('/resume/')
def resume():
    """
    Resume page
    Renders the resume template with professional data.
    """
    return render_template('resume.html', data=RESUME_DATA)

@app.route('/')
def home():
    """
    Homepage
    Redirects to the blog index.
    """
    from flask import redirect, url_for
    return redirect(url_for('blog.index'))

if __name__ == '__main__':
    # Use environment variable for port to be compatible with most hosting services
    port = int(os.environ.get("PORT", 5001))
    app.run(port=port, debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")
