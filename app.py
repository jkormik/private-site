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
        "name": "Йердан Счёвы",
        "title": "Full-Stack python-разработчик",
        "email": "999@bip.ru",
        "phone": "+7 (999) 999-99-99",
        "location": "Москва",
        "links": [
            {"name": "Telegram", "url": "https://t.me/bip", "icon": "telegram"},
            {"name": "GitHub", "url": "https://github.com/bip", "icon": "github"},
            {"name": "Portfolio", "url": "https://portfolio.example.com", "icon": "globe"},
        ]
    },
    "summary": "Разработчик с более чем 4-летним опытом построения масштабируемых веб-приложений. Знаток в области Python, Flask, Django, Selenium, с подтвержденным опытом ускорения у улучшения производительности систем.",
    "experience": [
        {
            "company": "SWG",
            "role": "Python-разработчик",
            "duration": "2022 - Present",
            "description": [
                "Вел разработку и внедрение комплексной системы мониторинга работоспособности веб-сайта. Система использовала Selenium для автоматизированного функционального тестирования ключевых путей пользователя (error tracking), обеспечивая проактивное обнаружение ошибок в реальном времени. Настроена интеграция с Telegram Bot API для моментального оповещения ответственных команд о выявленных инцидентах, что значительно сократило время реагирования на критические ошибки сайта.",
            "Запустил процесс ведения документации с автоматизированным доступом к информации, что на 20% повысило скорость онбординга новых сотрудников."
            ]
        },
        {
            "company": " RUFOOTAGE",
            "role": "Python-разработчик",
            "duration": "2020 - Present",
            "description": [
                "Разработал комплекс автоматизированную систему конвейерной обработки видеоматериала. Система обеспечивала полный цикл работы: от загрузки сырого видео до создания готового к продаже каталога.",
                "Реализовал модуль для медиа-обработки, интегрировав Python с FFmpeg для выполнения задач обрезки (trimming) и конвертации файлов в соответствии со стандартами стоков.",
                "Создал механизм генерации структурированных метаданных (JSON), позволяя каталогизировать видеоконтент и управлять его атрибутами.",
                "Спроектировал финальный ETL-процесс: преобразование JSON с описаниями в стандартизированные CSV-файлы, адаптированные под требования крупнейших стоков (Shutterstock, Pond5, Adobe Stock)."
            ]
        }
        ,
        {
            "company": " ALLFORDJ",
            "role": "Python-разработчик",
            "duration": "2017 - 2025",
            "description": [
                "Успешно разработал и внедрил систему для автоматического сбора, обработки и генерации новостного контента для онлайн-журнала Allfordj, обеспечив стабильный поток свежих материалов.",
                "Автоматизировал весь цикл: от мониторинга множества внешних источников (RSS) до получения готового текста статьи — тем самым повысив скорость наполнения сайта и расширив охват контента.",
                "Реализовал логику предварительной фильтрации полученного массива данных с помощью ключевых слов, значительно повысив релевантность контента.",
                "Осуществлял интеграцию программного модуля со сторонним API нейросетевой модели (NLP/LLM), передавая структурированные и отфильтрованные данные в качестве входных параметров для генерации статей.",
                "Создал систему, которая формировала черновики контента и направляла их на этап редакционной проверки, минимизируя ручное вмешательство и ускоряя цикл публикации материала."
            ]
        }
    ],
    "education": [
        {
            "institution": "Московский энергетический институт (Национальный исследовательский университет)",
            "degree": "Специалист по теоретической и прикладной лингвистике",
            "duration": "2008 - 2013"
        }
    ],
    "skills": {
        "Языки": ["Python", "JavaScript", "TypeScript", "SQL", "HTML/CSS"],
        "Фреймфорки": ["Flask", "Django", "FastAPI", "React", "Vue.js", "Tailwind CSS", "Selenium"],
        "Инструменты": ["Docker", "Kubernetes", "Git", "FFmpeg", "PostgreSQL", "Redis"],
        "Soft Skills": ["Лидерские качества", "Agile методология", "Стрессоустойчивость"]
    },
    "projects": [
        {
            "name": "CSVMonitorFast",
            "description": "Инструмент для парсинга и инализа категорий продуктов. Автоматизированный сбор данных, извлечение атрибутов, ежедневный мониторинг изменений версий сайта с оповещениями в Telegram.",
            "tech_stack": ["Python", "Selenium"],
            "link": "https://github.com/jkormik/csvmonitorfast"
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
