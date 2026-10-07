from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(50), nullable=False, default="student")
    status = db.Column(db.String(50), nullable=True, default="")

    def __repr__(self):
        return f'<User {self.fullname}>'

class Examination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(100), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)
    exam_status = db.Column(db.String(50), nullable=False, default='Draft')
    duration = db.Column(db.Integer, nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)
    slot_creation_start_date = db.Column(db.DateTime, nullable=False)
    slot_creation_end_date = db.Column(db.DateTime, nullable=False)
    slot_booking_start_date = db.Column(db.DateTime, nullable=False)
    slot_booking_end_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Examination {self.exam_name}>'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(50), nullable=False)
    course_status = db.Column(db.String(50), nullable=False, default='Inactive')
    course_description = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f'<Course {self.course_name}>'