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

with app.app_context():
    db.create_all()



# --- Blueprints ---
# Register the blog blueprint. 
# This makes the routes in blog/routes.py available under /blog
app.register_blueprint(blog_bp, url_prefix='/blog')
app.register_blueprint(admin_bp)


# --- Routes ---

# --- Resume Data ---
RESUME_DATA = {
    "personal_info": {
        "name": "Андрей Сычёв",
        "title": "Full-Stack python-разработчик",
        "email": "joshuakormik@yandex.ru",
        "phone": "+7 (962) 991-67-00",
        "location": "Москва",
        "links": [
            {"name": "Telegram", "url": "https://t.me/Jaunmia", "icon": "telegram"},
            {"name": "GitHub", "url": "https://github.com/jkormik", "icon": "github"},
            {"name": "Portfolio", "url": "https://portfolio.example.com", "icon": "globe"},
        ]
    },
    "summary": "Увлеченный рзработчик с более чем 4-летним опытом построения масштабируемых веб-приложений. Знаток в области Python, Flask, Django, Selenium и иных современных фреймворков, с подтвержденным опытом ускорения у улучшения производительности систем.",
    "experience": [
        {
            "company": "Centersvet",
            "role": "Python-разработчик",
            "duration": "2022 - Present",
            "description": [
                "Вел разработку и внедрение комплексной системы мониторинга работоспособности веб-сайта. Система использовала Selenium для автоматизированного функционального тестирования ключевых путей пользователя (error tracking), обеспечивая проактивное обнаружение ошибок в реальном времени. Настроена интеграция с Telegram Bot API для моментального оповещения ответственных команд о выявленных инцидентах, что значительно сократило время реагирования на критические ошибки сайта.",
            "Запустил процесс ведения документации с автоматизированным доступом к информации, что на 20% повысило скорость онбординга новых сотрудников."
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
            "institution": "Московский Энергетический Институт",
            "degree": "Специалист по теоретической и прикладной лингвистике",
            "duration": "2008 - 2013"
        }
    ],
    "skills": {
        "Языки": ["Python", "JavaScript", "TypeScript", "SQL", "HTML/CSS"],
        "Фреймфорки": ["Flask", "Django", "FastAPI", "React", "Vue.js", "Tailwind CSS", "Selenium"],
        "Инструменты": ["Docker", "Kubernetes", "Git", "AWS", "PostgreSQL", "Redis"],
        "Soft Skills": ["Лидерские качества", "Agile методология", "Стрессоустойчивость"]
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
