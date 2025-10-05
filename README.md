# NotionLite Flask — Notes + To-Do

A clean, modern Flask web app that combines **note-taking** and **to-do lists**, with user accounts, search, and a mobile-friendly UI.

## Features (MVP+)
- User auth (register/login/logout) with Flask-Login
- Notes (CRUD) with Markdown editor (SimpleMDE)
- Tasks (CRUD) with due date, priority, completion toggle
- Unified Dashboard (shows Notes + Tasks)
- Search across notes & tasks
- Dark mode toggle (remembered in localStorage)
- SQLite + SQLAlchemy (easy, portable)
- CSRF protection via Flask-WTF
- Bootstrap 5 + Bootstrap Icons (CDN)

## Quickstart

```bash
# 1) Create & activate a virtual environment (recommended)
python -m venv .venv
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app (development server)
# On Windows (PowerShell):
$env:FLASK_APP="wsgi.py"; $env:FLASK_DEBUG="1"; flask run
# On macOS/Linux:
export FLASK_APP=wsgi.py FLASK_DEBUG=1
flask run

# 4) Open in your browser
http://127.0.0.1:5000/
```

## Default Environment
- SQLite database at `instance/app.db` (auto-created)
- Secret key auto-generated if `.env` not used

## Optional: Environment Variables
Create a `.env` file in the project root to customize:
```
FLASK_SECRET_KEY=change-this-in-production
DATABASE_URL=sqlite:///instance/app.db
```

## Project Structure
```
notionlite_flask/
├─ app/
│  ├─ __init__.py
│  ├─ models.py
│  ├─ auth.py
│  ├─ routes.py
│  ├─ forms.py
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ index.html
│  │  ├─ notes.html
│  │  ├─ tasks.html
│  │  ├─ auth_login.html
│  │  ├─ auth_register.html
│  │  └─ _flash.html
│  └─ static/
│     └─ css/
│        └─ styles.css
├─ instance/           # created at runtime (holds app.db)
├─ requirements.txt
├─ wsgi.py
└─ README.md
```

## Notes
- This is a production-ready *starter*. For true production, use Gunicorn/uvicorn behind a reverse proxy and a managed Postgres.
- You can wrap this web app as a desktop app using Electron/Tauri, or as a mobile app via a WebView wrapper.
