import os
import re
import sqlite3
from pathlib import Path
from functools import wraps

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "college_faq.db"

load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "Please set FLASK_SECRET_KEY in your .env file."
    )

# Login Required Decorator

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "student_id" not in session:
            flash("Please register or login to access this service.")
            return redirect(
                url_for("login", next=request.path)
            )

        return view(*args, **kwargs)

    return wrapped_view

# Database Helpers

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_student_db():
    """Create students table if it does not exist."""
    conn = get_db_connection()

    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def get_answer(question):
    question = question.lower().strip()
    question = re.sub(r"[^\w\s]", " ", question)
    question = re.sub(r"\s+", " ", question)

    if not question:
        return "Please enter your question."

    conn = get_db_connection()
    try:
        faqs = conn.execute("SELECT * FROM faqs").fetchall()
    finally:
        conn.close()

    best_answer = None
    best_score = 0

    for faq in faqs:
        keywords = faq["keywords"].lower().split()
        score = 0

        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, question):
                score += 1

        if score > best_score:
            best_score = score
            best_answer = faq["answer"]

    if best_answer is not None and best_score > 0:
        return best_answer

    return (
        "Sorry, I could not find a reliable answer. "
        "Please contact your college office or check "
        "the official college website."
    )


init_student_db()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/courses")
@login_required
def courses():
    items = [
        "Bachelor of Computer Applications (BCA)",
        "Bachelor of Business Administration (BBA)",
        "Bachelor of Commerce (B.Com)",
        "Bachelor of Science (B.Sc)",
        "Bachelor of Arts (B.A)",
        "Master of Computer Applications (MCA)",
        "Master of Business Administration (MBA)",
    ]

    return render_template(
        "courses.html",
        title="Courses",
        description="Explore college courses and program information.",
        items=items,
    )


@app.route("/admissions")
@login_required
def admissions():
    return render_template(
        "admission.html",
        title="Admissions",
    )


@app.route("/exams")
@login_required
def exams():
    return render_template(
        "exams.html",
        title="Exams Information",
    )


@app.route("/services")
@login_required
def services():
    return render_template(
        "services.html",
        title="Student Services",
    )


@app.route("/scholarship")
@login_required
def scholarship():
    return render_template(
        "scholarship.html",
        title="Scholarship Information",
    )



@app.route("/chatbot")
@login_required
def chatbot():
    return render_template("chatbot.html")

@app.route("/ask", methods=["POST"])
@login_required
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")

    if not isinstance(question, str) or not question.strip():
        return jsonify({
            "answer": "Please enter a question."
        }), 400

    answer = get_answer(question)

    return jsonify({"answer": answer})
    

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    message = ""

    if request.method == "POST":
        keywords = request.form.get(
            "keywords", ""
        ).strip().lower()

        answer = request.form.get(
            "answer", ""
        ).strip()

        if not keywords or not answer:
            message = "Please enter both keywords and answer."

        else:
            conn = get_db_connection()

            try:
                conn.execute(
                    """
                    INSERT INTO faqs (keywords, answer)
                    VALUES (?, ?)
                    """,
                    (keywords, answer),
                )

                conn.commit()
                message = "FAQ saved successfully!"

            except sqlite3.Error:
                app.logger.exception(
                    "Could not save FAQ."
                )

                message = (
                    "Could not save the FAQ. "
                    "Check whether the FAQs table exists."
                )

            finally:
                conn.close()

    return render_template(
        "admin.html",
        message=message,
    )
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill all fields.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash(
                "Password must be at least 8 characters."
            )
            return redirect(url_for("register"))

        conn = get_db_connection()

        try:
            conn.execute(
                """
                INSERT INTO students
                    (name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    generate_password_hash(password),
                ),
            )

            conn.commit()

        except sqlite3.IntegrityError:
            flash("This email is already registered.")
            return redirect(url_for("register"))

        except sqlite3.Error:
            app.logger.exception(
                "Registration database error."
            )

            flash(
                "Registration failed due to a database error."
            )
            return redirect(url_for("register"))

        finally:
            conn.close()

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get("password", "")

        conn = get_db_connection()

        try:
            student = conn.execute(
                """
                SELECT id, name, email, password_hash
                FROM students
                WHERE email = ?
                """,
                (email,),
            ).fetchone()

        except sqlite3.Error:
            app.logger.exception("Login database error.")
            flash("Login is temporarily unavailable.")
            return render_template("login.html")

        finally:
            conn.close()

        if student and check_password_hash(
            student["password_hash"], password
        ):
            session.clear()

            session["student_id"] = student["id"]
            session["student_name"] = student["name"]

            return redirect(
                url_for("student_dashboard")
            )

        flash("Invalid email or password.")

    return render_template("login.html")


@app.route("/student-dashboard")
@login_required
def student_dashboard():
    return render_template(
        "student_dashboard.html",
        name=session.get("student_name", "Student"),
    )


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have been logged out.")

    return redirect(url_for("login"))
    

if __name__ == "__main__":
    app.run(debug=True)
