## I. 🚀 Project Overview & Goal Definition

**Project Name:** Private Resume Site & Blog
**Goal:** To develop a fully functional, single-domain site that presents highly polished personal resume data and hosts a dynamic, navigable blog. The system must be secure (private/auth-protected) and performant.
**Target Audience:** Recruiters, industry peers (Reading audience). Content editors (Writing audience).

### Core Modules:
1.  **Homepage (`/`):** Presents the polished, static professional resume. This is the primary landing page.
2.  **Blog Index (`/blog`):** Displays a listing of all blog posts with titles, dates, and short excerpts.
3.  **Single Post View (`/blog/<slug>`):** Displays the full content of an individual post.
4.  **Admin Interface (Internal):** A protected section for managing database entries (creating/editing posts).

## II. 🛠️ Technical Stack & Architectural Constraints

### A. Core Languages & Frameworks
*   **Backend:** Python 3.10+
*   **Web Framework:** Flask (Flask must be used, no other framework.)
*   **Data Management:** SQLAlchemy ORM (Used for all persistent data).
*   **Styling:** Tailwind CSS (Must use utility-first approach exclusively for styling. Do not write custom CSS blocks unless absolutely necessary).

### B. Dependency Management Constraint ⚠️ (CRITICAL)
***When creating or updating dependency files (`requirements.txt`) or providing setup instructions, you MUST assume and recommend the use of `uv` for dependency management over `pip` or `venv`.***
*   **Incorrect:** "Use pip to install..."
*   **Correct:** "Initialize dependencies using `uv add ...`."

### C. File Structure Mapping (Mandatory Adherence)
All pathing and file placement must adhere strictly to this structure:

| Folder | Purpose | Content/Usage | Constraints |
| :--- | :--- | :--- | :--- |
| `templates/` | **Presentation Layer** | Contains all Jinja2 templates (`.html`). Never execute Python logic here; only render variables. | Must use `{% extends "base.html" %}` for inheritance. |
| `static/` | **Assets** | CSS (compiled Tailwind output), JavaScript, images. | All paths must be referenced using `{{ url_for('static', filename='...')') }}`. |
| `blog/` | **Data Source/Models** | Used conceptually to manage blog data models or structured content directories (if not purely database-driven). | For DB operations, this folder holds the ORM definitions (`models.py`). |

## III. 📝 Code Quality & Standards Guidelines

### A. Python Best Practices
1.  **Separation of Concerns:** Keep database logic (SQLAlchemy setup) isolated from routing logic (`app.py`) where possible. Use dedicated module files for models.
2.  **Asynchronous Handling:** Assume performance may be a concern; structure endpoints to be efficient.
3.  **Code Style:** Follow standard PEP 8 guidelines religiously. Use clear variable names (e.g., `blog_post` instead of `bp`).
4.  **Error Handling:** All external-facing routes must include robust `try...except` blocks to handle potential database or file access errors gracefully, providing a friendly error message rather than a traceback.

### B. Frontend & UI/UX Standards (Tailwind CSS)
1.  **Responsiveness First:** All components *must* be designed with mobile-first principles. Use Tailwind breakpoints (`sm:`, `md:`, `lg:`) to guarantee proper rendering on small screens first.
2.  **Accessibility (A11y):** Ensure all interactive elements (buttons, links) have sufficient color contrast and are properly labeled for screen readers where applicable.
3.  **Theming:** The primary style must be clean, minimalist, professional, and high-contrast (e.g., dark text on light background). Use neutral palettes with one accent color.

### C. Flask Routing Guidelines
1.  Use **Blueprints** for modularity (e.g., create a `blog_bp` blueprint to handle all blog routes instead of cluttering the main `app.py`).
2.  Ensure every request has clear docstrings explaining its input parameters and expected output/return state.

## IV. 💡 Pi's Operational Protocol (How I Expect You to Act)

When I give you a task, you must follow this protocol:

1.  **Analyze:** First, confirm the technical requirements and scope of the requested feature. *Always ask clarifying questions if ambiguity exists.*
2.  **Plan:** Before writing code, generate a brief plan (e.g., "I will update `app.py` to modify the `/blog` route, create a new template in `templates/`, and add SQLAlchemy migration logic.").
3.  **Execute & Explain:** Write only the necessary, minimal code block required. Following the code, provide a clear **Explanation** section detailing:
    *   *What* the code does.
    *   *Where* it must be placed (e.g., "Update `templates/base.html`").
    *   *Any prerequisites* (e.g., "You must first run `uv sync` in the root directory.").