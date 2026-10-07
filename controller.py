from datetime import datetime

from flask import flash, render_template,request,redirect,url_for,session
from models import Course, db, User,Examination




def signin():
    email = request.form.get("emailId")
    password = request.form.get("password")

    if email == "" or password == "":
        flash('All fields are required!', 'danger')
        return redirect(url_for('users.login'))

    user = User.query.filter_by(email = email, password = password).first()

    if user:
        session['user_id'] = user.id
        session['role'] = user.role
        return redirect(url_for('dashboard.get_stats'))
    
    else:
        flash('Invalid email or password!', 'danger')
        return redirect(url_for('users.login'))

def signup():
    fullname = request.form.get("fullName")
    email = request.form.get("emailId")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmPassword")
    role = request.form.get("role")

    if fullname == "" or email == "" or password == "" or confirm_password == "" or role == "":
        flash('All fields are required!', 'danger')
        return redirect(url_for('users.register'))

    if password != confirm_password:
        flash('Password and Confirm password must be same!', 'danger')
        return redirect(url_for('users.register'))

    if User.query.filter_by(email = email).first():
        flash('Email already exists!', 'danger')
        return redirect(url_for('users.register'))

    if role == "examiner":
        user = User(fullname = fullname,
                    email = email, 
                    password = password,
                    role = "examiner",
                    status = "pending")
    else:
        user = User(fullname = fullname,
                    email = email, 
                    password = password,
                    role = "student") 
        
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users.login'))

def logout_func():
    session.clear()
    return redirect(url_for("users.login"))


def stats():
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    return render_template(
        "Stats.html",
        role=session["role"]
    )

def examination():
    if "user_id" not in session:
        return redirect(url_for("users.login"))


    exam_name = request.form.get("exam_name")
    duration = request.form.get("duration") 
    max_marks = request.form.get("max_marks")
    exam_type = request.form.get("exam_type")
    status = request.form.get("status")
    slot_creation_start_date = request.form.get("slot_creation_start_date")
    slot_creation_end_date = request.form.get("slot_creation_end_date")
    slot_booking_start_date = request.form.get("slot_booking_start_date")
    slot_booking_end_date = request.form.get("slot_booking_end_date")

    # Convert string dates to datetime objects
    scsd= datetime.strptime(slot_creation_start_date, "%Y-%m-%d")
    sced= datetime.strptime(slot_creation_end_date, "%Y-%m-%d")
    sbsd= datetime.strptime(slot_booking_start_date, "%Y-%m-%d")
    sbed= datetime.strptime(slot_booking_end_date, "%Y-%m-%d")

    examination_data = {
        "exam_name": exam_name,
        "exam_type": exam_type,
        "exam_status": status,
        "duration": duration,
        "max_marks": max_marks,
        "slot_creation_start_date": scsd,
        "slot_creation_end_date": sced,
        "slot_booking_start_date": sbsd,
        "slot_booking_end_date": sbed
    }

    exam = Examination(**examination_data)
    db.session.add(exam)
    db.session.commit()
    flash('Examination created successfully!', 'success')
    return redirect(url_for('dashboard.get_examination'))

def courses():
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    course_name = request.form.get("course_name")
    course_code = request.form.get("course_code")
    course_description = request.form.get("course_description")
    course_status = request.form.get("course_status")

    course_data = {
        "course_name": course_name,
        "course_code": course_code,
        "course_status": course_status,
        "course_description": course_description
    }

    course = Course(**course_data)
    db.session.add(course)
    db.session.commit()
    flash('Course created successfully!', 'success')
    return redirect(url_for('dashboard.get_courses'))
