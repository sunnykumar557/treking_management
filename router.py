import functools
from flask import Blueprint, redirect,request,render_template, session, url_for,flash
from controller import examination, logout_func, signin,signup,courses,stats
from models import Examination,db,User,Course

user_bp = Blueprint("users",__name__,url_prefix = "/users")
dashboard_bp = Blueprint("dashboard",__name__,url_prefix = "/dashboard")

def check_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("users.login"))
        if session["role"] != "admin":
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("dashboard.get_stats"))
        return func(*args, **kwargs)
    return wrapper



@user_bp.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "GET":
        if "user_id" in session:
            return redirect(url_for("dashboard.get_stats"))
        else:
            return render_template("register.html")
    if request.method == "POST":
        return signup()

@user_bp.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "GET":
        if "user_id" in session:
            return redirect(url_for("dashboard.get_stats"))
        else:
            return render_template("login.html")
    if request.method == "POST":
        return signin()

@user_bp.route("/logout",methods = ["GET"])
def logout():
    return logout_func()


@dashboard_bp.route("/stats",methods = ["GET"])
def get_stats():
    return stats()


@dashboard_bp.route("/examiners",methods = ["GET","POST"])
@check_admin
def get_examiners():
    if request.method == "GET":
        if "user_id" not in session:
            return redirect(url_for("users.login"))
        else:
            users = User.query.all()
            return render_template(
                "Examiners.html",
                users=users
            )

@dashboard_bp.route("/students",methods = ["GET","POST"])
@check_admin
def get_students():
    if request.method == "GET":
        if "user_id" not in session:
            return redirect(url_for("users.login"))
        else:
            users = User.query.all()
            return render_template(
                "Students.html",
                users=users
            )

@dashboard_bp.route("/examination",methods = ["GET","POST"])
@check_admin
def get_examination():
    if request.method == "GET":
        if "user_id" not in session:
            return redirect(url_for("users.login"))
        else:
            exam_data = Examination.query.all()
            return render_template(
                "Examination.html",
                exam_data=exam_data
            )

    if request.method == "POST":
        return examination()

@dashboard_bp.route("/delete_examination/<int:exam_id>",methods = ["GET"])
@check_admin
def delete_examination(exam_id):
    if "user_id" not in session:
        return redirect(url_for("users.login"))
    else:
        exam = Examination.query.filter_by(id=exam_id).first()
        if exam:
            db.session.delete(exam)
            db.session.commit()
            return redirect(url_for("dashboard.get_examination"))
    
@dashboard_bp.route("/courses",methods = ["GET","POST"])
@check_admin
def get_courses():
    if request.method == "GET":
        if "user_id" not in session:
            return redirect(url_for("users.login"))
        else:
            courses_data = Course.query.all()
            return render_template(
                "Courses.html",
                courses_data=courses_data
            )
    if request.method == "POST":
        return courses()

@dashboard_bp.route("/delete_course/<int:course_id>",methods = ["GET"])
@check_admin
def delete_course(course_id):
    if "user_id" not in session:
        return redirect(url_for("users.login"))
    else:
        course = Course.query.filter_by(id=course_id).first()
        if course:
            db.session.delete(course)
            db.session.commit()
            return redirect(url_for("dashboard.get_courses"))

@dashboard_bp.route("/approve_status/<int:examiner_id>", methods=["GET"])
@check_admin
def approve_status(examiner_id):
    if "user_id" not in session:
        return redirect(url_for("users.login"))
    
    examiner = User.query.filter_by(id=examiner_id).first()
    examiner.status = "approved"
    db.session.commit()
    return redirect(url_for('dashboard.get_examiners'))

@dashboard_bp.route("/reject_status/<int:examiner_id>", methods=["GET"])
@check_admin
def reject_status(examiner_id):
    if "user_id" not in session:
        return redirect(url_for("users.login"))
    
    examiner = User.query.filter_by(id=examiner_id).first()
    examiner.status = "rejected"
    db.session.commit()
    return redirect(url_for('dashboard.get_examiners'))

    



