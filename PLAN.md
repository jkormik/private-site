## 🚀 Site Development Plan: Resume & Blog

### 💡 Goal Summary
To build a single-page application/site that presents professional resume content and hosts a dynamically updated blog, using Python/Flask for backend logic and Tailwind CSS for modern styling.

### 🛠️ Suggested Tooling / Libraries
Since you are using Flask, here are some recommended libraries to save time:

1.  **Database:** SQLite (Easiest setup for local development).
2.  **ORM (Object-Relational Mapper):** SQLAlchemy (Excellent pairing with Flask).
3.  **Forms/Security:** Flask-WTF (Simplifies form creation and handling).
4.  **Styling Helper:** Tailwind CSS CLI or a dedicated build process (Make sure your Python environment compiles the tailwind classes into actual CSS files for `static/`).

---

## 📅 Phase 1: Setup & Foundation (The Infrastructure)

*Goal: Get the basic app running and structure defined.*
*(Time estimate: Low)*

| Task | Focus Area | Details / Action Items | Files Impacted |
| :--- | :--- | :--- | :--- |
| **1. Project Initialization** | Backend Setup | Install Flask, SQLAlchemy, etc. Initialize the basic `app.py` file. | `/app.py`, `requirements.txt` |
| **2. Folder Structure Check** | File Organization | Ensure your directories are correctly configured: `templates/` (HTML), `static/` (CSS/JS images), `blog/` (where blog content models or data might live). | All folders |
| **3. Basic Layout Template** | Frontend Core | Create a base template (`base.html`) in the `templates/` folder. This file will contain your common `<head>` tags, navigation bar structure, and include directives for child pages. **Include the link to compiled Tailwind CSS here.** | `templates/base.html`, `static/css/styles.css` |
| **4. Basic Routing** | Backend Logic | Implement two simple routes: `/` (Homepage) and `/blog` (Blog Index). These routes should just return "Hello World" for now. | `app.py` |

---

## ⭐️ Phase 2: The Resume Site MVP (Static Presentation)

*Goal: Build the core, read-only resume component.*
*(Time estimate: Medium)*

This is the most critical part—it needs to look perfect and be simple. Since professional resumes are generally static data, you won't need a database for this initial version; hardcoding/defining the structure in Python variables or using a YAML file is easiest.

| Task | Focus Area | Details / Action Items | Files Impacted |
| :--- | :--- | :--- | :--- |
| **1. Data Modeling** | Backend Logic | Create a structured dictionary or class instance in `app.py` to hold all personal information (Name, Contact Info, Summary). | `app.py` (or data file) |
| **2. The Resume Template** | Frontend Design | Build the main resume page template (`templates/resume.html`). Use Tailwind classes extensively here for clean layout, spacing, and typography. Focus on readability over complexity. | `templates/resume.html` |
| **3. Component Rendering** | Backend Logic | Modify the `/` route to render `resume.html`, passing in the structured data (Name, Experience List, Education List) defined in Step 1. | `app.py`, `templates/resume.html` |
| **4. Navigation & Polish** | Frontend Design | Integrate a persistent navigation bar into `base.html` linking to Home (`/`) and Blog (`/blog`). Ensure the resume content is mobile-responsive using Tailwind breakpoints. | `templates/base.html` |

---

## 📰 Phase 3: The Blog Feature (Dynamic Content)

*Goal: Implement dynamic reading, writing, and listing of blog posts.*
*(Time estimate: High)*

This phase introduces database management and user interaction.

| Task | Focus Area | Details / Action Items | Files Impacted |
| :--- | :--- | :--- | :--- |
| **1. Database Setup** | Backend Logic | Initialize SQLAlchemy. Define a `BlogPost` model (Title, Slug/URL, Date, Content/Body). Set up the database connection and create initial tables. | `app.py`, SQLAlchemy models |
| **2. Blog Post Creation (Admin)** | Back-End Write Path | Create an Admin route (e.g., `/admin/new_post`). Use Flask-WTF to handle form submission, allowing you to input a title, date, and content body. This function saves the data to the database. ***(Crucial Security Note: Implement basic authentication here!)*** | `app.py`, `templates/admin/create_post.html` |
| **3. Blog Listing Page** | Backend Read Path | Update the `/blog` route handler. It should query *all* blog posts from the database and pass them to a template. | `app.py`, `templates/blog/index.html` |
| **4. Individual Post View** | Frontend Design | Create `templates/blog/post.html`. This template accepts a single post object (via the URL) and displays its full content, title, date, and comments section structure. | `app.py`, `templates/blog/post.html` |

---

## ✨ Phase 4: Polish, UX, & Deployment

*Goal: Final professional touches, making it robust.*
*(Time estimate: Medium)*

| Task | Focus Area | Details / Action Items | Files Impacted |
| :--- | :--- | :--- | :--- |
| **1. SEO/Metadata** | Frontend Polish | Add proper `<meta>` tags to `base.html` for all pages (description, keywords). Consider Open Graph tags for social sharing previews. | `templates/base.html` |
| **2. User Experience (UX) Review** | Testing & Styling | Conduct thorough browser testing: check appearance on mobile, tablet, and desktop. Use Tailwind's utility classes to improve transitions or subtle hover effects. | All Templates |
| **3. Deployment Readiness** | Backend Logic | Create a clear `Procfile` (if using services like Heroku/Render) that tells the server how to run your Flask application. Test environment variables needed for database connection. | Root folder, `.env` file |
| **4. Private Access Control** | Security | Implement simple authentication decorators (`@login_required`) on any administrative routes (creating or editing posts). For a *private* site, this might be a basic username/password check. | `app.py` |

---

## 📋 Development Workflow Checklist (Action Plan)

Follow these steps sequentially to maximize momentum:

1.  **Setup:** Complete Phase 1 (Can I run the app and see a base page?).
2.  **MVP:** Complete Phase 2 (Is my resume looking fantastic on mobile?). *Test this thoroughly before touching the blog.*
3.  **Data Source:** Create your SQLAlchemy models and connect them to Flask. Run migration scripts.
4.  **Write Path:** Build the admin/CMS feature first (how do I get data into the system?). **(Phase 3, Step 2)**
5.  **Read Path:** Use that saved data to build the listing page and individual post view. **(Phase 3, Steps 3 & 4)**
6.  **Review:** Tidy up navigation, fix minor CSS bugs, and implement security measures. **(Phase 4)**

Good luck with your development! Stick to one phase at a time, and you will successfully launch this site.