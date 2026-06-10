from flask import Flask, render_template
from extensions import db
from blog.routes import blog_bp
from admin.routes import admin_bp
import blog.models # Ensure models are registered with SQLAlchemy



# Initialize Flask Application
app = Flask(__name__)

# --- Configuration ---
# Using SQLite for local development as per PLAN.md
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-this-in-production'

# Initialize SQLAlchemy
db.init_app(app)


# --- Blueprints ---
# Register the blog blueprint. 
# This makes the routes in blog/routes.py available under /blog
app.register_blueprint(blog_bp, url_prefix='/blog')
app.register_blueprint(admin_bp)


# --- Routes ---

# --- Resume Data ---
RESUME_DATA = {
    "personal_info": {
        "name": "Alex Shepherd",
        "title": "Senior Full-Stack Engineer",
        "email": "alex.shepherd@example.com",
        "phone": "+1 (555) 000-0000",
        "location": "New York, NY",
        "links": [
            {"name": "LinkedIn", "url": "https://linkedin.com/in/username", "icon": "linkedin"},
            {"name": "GitHub", "url": "https://github.com/username", "icon": "github"},
            {"name": "Portfolio", "url": "https://portfolio.example.com", "icon": "globe"},
        ]
    },
    "summary": "Dedicated software engineer with over 8 years of experience building scalable web applications. Expert in Python, Flask, and modern frontend frameworks, with a proven track record of improving system performance and leading cross-functional teams.",
    "experience": [
        {
            "company": "TechInnovate Solutions",
            "role": "Senior Software Engineer",
            "duration": "2020 - Present",
            "description": [
                "Led the migration of a monolithic legacy system to a microservices architecture, reducing deployment time by 40%.",
                "Optimized database queries using SQLAlchemy and Redis, improving page load speeds by 200ms.",
                "Mentored 5 junior developers and established a new code review process that reduced production bugs by 15%."
            ]
        },
        {
            "company": "WebFlow Dynamics",
            "role": "Full-Stack Developer",
            "duration": "2017 - 2020",
            "description": [
                "Developed a real-time analytics dashboard using Flask and WebSocket, used by 50+ corporate clients.",
                "Implemented a comprehensive CI/CD pipeline using GitHub Actions and AWS, ensuring zero-downtime deployments.",
                "Collaborated with UI/UX designers to implement a fully responsive interface using Tailwind CSS."
            ]
        }
    ],
    "education": [
        {
            "institution": "University of Technology",
            "degree": "B.S. in Computer Science",
            "duration": "2013 - 2017",
            "honor": "Summa Cum Laude"
        }
    ],
    "skills": {
        "Languages": ["Python", "JavaScript", "TypeScript", "SQL", "HTML/CSS"],
        "Frameworks": ["Flask", "FastAPI", "React", "Vue.js", "Tailwind CSS"],
        "Tools": ["Docker", "Kubernetes", "Git", "AWS", "PostgreSQL", "Redis"],
        "Soft Skills": ["Team Leadership", "Agile Methodology", "Technical Writing"]
    },
    "projects": [
        {
            "name": "OpenSource Project X",
            "description": "A high-performance distributed task queue implemented in Python.",
            "tech_stack": ["Python", "Redis", "Docker"],
            "link": "https://github.com/username/project-x"
        },
        {
            "name": "E-Commerce Engine",
            "description": "A custom-built headless commerce API supporting multi-currency and global shipping.",
            "tech_stack": ["Flask", "PostgreSQL", "Stripe API"],
            "link": "https://github.com/username/ecommerce-engine"
        }
    ]
}

# --- Routes ---

@app.route('/')
def home():
    """
    Homepage
    Renders the resume template with professional data.
    """
    return render_template('resume.html', data=RESUME_DATA)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create database tables based on models
    app.run(debug=True)
