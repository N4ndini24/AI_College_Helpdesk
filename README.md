# AI_College_Helpdesk
AI College Helpdesk is a Flask-based web application that helps students access college information, courses, admissions, exams, scholarships, and services. It includes a chatbot for answering student queries, secure login and registration, and an admin feature to manage frequently asked questions using an SQLite database.

## Features

- Student registration and login
- Password hashing with Werkzeug (included with Flask)
- Student dashboard and logout
- Course, admission, exam, scholarship, and student-service pages
- FAQ chatbot endpoint (`/ask`)
- Admin page for adding FAQs
- SQLite database

## Requirements

- Python 3.10 or newer recommended
- pip
- Git (optional, for uploading to GitHub)

## 1. Download or clone the project

If the project is on GitHub:

```bash
git clone https://github.com/YOUR_USERNAME/AI_College_Helpdesk.git
cd AI_College_Helpdesk
```

Or open the project folder you already have on your computer.

## 2. Create and activate a virtual environment

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Create your `.env` file

Create a file named `.env` in the same folder as `app.py`. Add a new secret key:

```env
FLASK_SECRET_KEY=replace_this_with_a_new_random_secret_key
```

Generate a secure key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value after `FLASK_SECRET_KEY=` in `.env`.

**Security:** Never upload `.env` to GitHub or share your secret key publicly. Make sure `.env` is listed in `.gitignore`.

## 5. Initialize the database and add sample FAQs

Run these commands from the project root, with the virtual environment activated:

```bash
python init_student_db.py
python add_faq.py
```

`init_student_db.py` creates the required SQLite tables. `add_faq.py` inserts the sample FAQs and skips matching entries that already exist.

The database file is expected to be named `college_faq.db` in the same folder as `app.py`.

## 6. Run the application locally

```bash
python app.py
```

Open the local URL shown in the terminal, usually:

http://127.0.0.1:5000

Press `Ctrl+C` in the terminal to stop the server.

## Important template filenames

Flask's `render_template()` calls must match the actual filenames inside `templates/`. Based on the current `app.py`, check that these files exist:

- `index.html`
- `courses.html`
- `admission.html`
- `exams.html`
- `services.html`
- `scholarship.html`
- `chatbot.html`
- `admin.html`
- `register.html`
- `login.html`
- `student_dashboard.html`

If a file has a different name (for example, `student_dashbord.html`), either rename it or update the corresponding `render_template()` call in `app.py`.

## Deploying online

Typical Render settings:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`
- **Environment variable:** `FLASK_SECRET_KEY` set to a new secure value

## Troubleshooting

- **`Please set FLASK_SECRET_KEY`**: Check that `.env` is beside `app.py` and contains `FLASK_SECRET_KEY=...`.
- **`ModuleNotFoundError: dotenv`**: Activate the correct virtual environment, then run `python -m pip install -r requirements.txt`.
- **`TemplateNotFound`**: Check the filename in `templates/` against the matching `render_template()` call.
- **FAQ table missing or database error**: Run `python init_student_db.py` first, then `python add_faq.py`.
- **`git push` fails**: Confirm the repository URL and that you have permission to push to it.
