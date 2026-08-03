import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Application
from sqlalchemy import or_


app = Flask(
    __name__,
    template_folder=".",
    static_folder=".",
    static_url_path=""
)

app.config.from_object(Config)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)


@app.route("/")
def home():
    return "Job Tracker Running"


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not full_name or not email or not password:
            return "Please fill all fields"

        hashed_password = generate_password_hash(password)

        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            
            session["user_id"] = user.id
            session["user_name"] = user.full_name

            return redirect(url_for("dashboard"))
        

        return "Invalid email or password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    total = Application.query.filter_by(user_id=user_id).count()

    applied = Application.query.filter_by(
        user_id=user_id,
        status="Applied"
    ).count()

    assessment = Application.query.filter_by(
        user_id=user_id,
        status="Assessment"
    ).count()

    interview = Application.query.filter_by(
        user_id=user_id,
        status="Interview"
    ).count()

    offer = Application.query.filter_by(
        user_id=user_id,
        status="Offer"
    ).count()

    rejected = Application.query.filter_by(
        user_id=user_id,
        status="Rejected"
    ).count()

    recent_applications = Application.query.filter_by(
        user_id=user_id
    ).order_by(
        Application.id.desc()
    ).limit(5).all()
    upcoming_interviews = Application.query.filter(
    Application.user_id == user_id,
    Application.status == "Interview"
    ).order_by(
        Application.interview_date
    ).limit(5).all()
    return render_template(
        "dashboard.html",
        total=total,
        applied=applied,
        assessment=assessment,
        interview=interview,
        offer=offer,
        rejected=rejected,
        recent_applications=recent_applications,
        upcoming_interviews=upcoming_interviews
    )

@app.route("/add", methods=["GET", "POST"])
def add_application():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        company = request.form.get("company")
        role = request.form.get("role")
        location = request.form.get("location")
        job_type = request.form.get("job_type")
        application_date = request.form.get("application_date")
        status = request.form.get("status")
        portal = request.form.get("portal")
        notes = request.form.get("notes")
        interview_date = request.form.get("interview_date") or None


        # Resume upload
        resume = request.files.get("resume")

        resume_filename = None

        if resume and resume.filename:
            resume_filename = secure_filename(resume.filename)

            resume.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    resume_filename
                )
            )


        new_application = Application(
            company=company,
            role=role,
            location=location,
            job_type=job_type,
            application_date=application_date,
            status=status,
            portal=portal,
            notes=notes,
            interview_date=interview_date,
            resume_file=resume_filename,
            user_id=session["user_id"]
        )

        db.session.add(new_application)
        db.session.commit()

        return redirect(url_for("view_applications"))

    return render_template("add_application.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


@app.route("/applications")
def view_applications():

    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    sort = request.args.get("sort", "")

    query = Application.query.filter_by(
        user_id=session["user_id"]
    )

    if search:

        query = query.filter(

            or_(

                Application.company.ilike(f"%{search}%"),

                Application.role.ilike(f"%{search}%")

            )

        )
    if status:
         query = query.filter(Application.status == status)
    if sort == "newest":
         query = query.order_by(Application.application_date.desc())

    elif sort == "oldest":
         query = query.order_by(Application.application_date.asc())

    elif sort == "company_asc":
          query = query.order_by(Application.company.asc())

    elif sort == "company_desc":
         query = query.order_by(Application.company.desc())
    applications = query.all()

    return render_template(
        "view_applications.html",
        applications=applications
    )


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    application = Application.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first_or_404()

    if request.method == "POST":

        application.company = request.form.get("company")
        application.role = request.form.get("role")
        application.location = request.form.get("location")
        application.job_type = request.form.get("job_type")
        application.application_date = request.form.get("application_date")
        application.status = request.form.get("status")
        application.portal = request.form.get("portal")
        application.notes = request.form.get("notes")
        application.interview_date = request.form.get("interview_date") or None
        resume = request.files.get("resume")

        if resume and resume.filename:

            resume_filename = secure_filename(resume.filename)

            resume.save(
            os.path.join(
            app.config["UPLOAD_FOLDER"],
            resume_filename
        )
    )

            application.resume_file = resume_filename

        db.session.commit()

        return redirect(url_for("view_applications"))

    return render_template(
        "edit_application.html",
        application=application
    )

@app.route("/delete/<int:id>")
def delete_application(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    application = Application.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first_or_404()

    db.session.delete(application)
    db.session.commit()

    return redirect(url_for("view_applications"))

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)