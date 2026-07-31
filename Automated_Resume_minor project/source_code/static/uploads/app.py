from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

from models.database import init_db
from analyzer.parser import extract_text
from analyzer.score import calculate_score
from analyzer.ats import ats_score
from analyzer.suggestions import get_missing_skills

app = Flask(__name__)
app.secret_key = "resume_analyzer_secret_key"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()


def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = get_connection()
        cur = conn.cursor()

        try:

            cur.execute(
                """
                INSERT INTO users(name,email,password)
                VALUES(?,?,?)
                """,
                (name, email, password)
            )

            conn.commit()

            flash("Registration Successful!")

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            flash("Email already exists!")

        except Exception as e:

            print(e)
            flash(str(e))

        finally:

            conn.close()

    return render_template("register.html")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user"] = user["email"]

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password")

    return render_template("login.html")


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# ---------------- UPLOAD ---------------- #

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        if "resume" not in request.files:

            flash("Please upload a resume.")
            return redirect(url_for("upload"))

        file = request.files["resume"]
        job_role = request.form["job_role"]

        if file.filename == "":

            flash("Please select a resume.")
            return redirect(url_for("upload"))

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        resume_text = extract_text(filepath)

        score, skills = calculate_score(
            resume_text,
            job_role
        )

        ats = ats_score(score)

        missing = get_missing_skills(skills)

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO resumes
            (user_email, filename, score)
            VALUES (?, ?, ?)
            """,
            (
                session["user"],
                file.filename,
                score
            )
        )

        conn.commit()
        conn.close()

        return render_template(
            "result.html",
            score=score,
            skills=skills,
            ats=ats,
            missing=missing,
            job_role=job_role
        )

    return render_template("upload.html")


# ---------------- HISTORY ---------------- #

@app.route("/history")
def history():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_connection()

    history = conn.execute(
        """
        SELECT *
        FROM resumes
        WHERE user_email=?
        ORDER BY uploaded_at DESC
        """,
        (session["user"],)
    ).fetchall()

    conn.close()

    return render_template(
        "history.html",
        history=history
    )


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.pop("user", None)

    flash("Logged out successfully.")

    return redirect(url_for("home"))


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)