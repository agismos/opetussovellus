from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def list_courses():
    sql = text("SELECT course_name FROM courses")
    result = db.session.execute(sql)
    courses = result.fetchall()
    result = ""
    for course in courses:
        result += f"<a href='/show_course_details/{course[0]}'>" + f"{course[0]}" + "</a><br>"
    return result

def course_information(course_name):
    sql = text(f"SELECT contents FROM courses WHERE course_name='{course_name}'")
    db.session.execute(text("SET client_encoding TO 'UTF8';"))
    result = db.session.execute(sql)
    details = result.fetchone()
    return details[0]

def add_student(course_name):
    student_username = session['username']

    sql = text(f"SELECT (teacher_username) FROM courses WHERE course_name='{course_name}'")
    teacher_username = db.session.execute(sql).fetchone()[0]

    sql = text(f"SELECT (id) FROM courses WHERE course_name='{course_name}'")
    course_id = db.session.execute(sql).fetchone()[0]

    sql = text(f"INSERT INTO enrollments (course_id, course_name, student_username, \
               teacher_username) VALUES (:course_id, :course_name, :student_username, \
               :teacher_username)")
    
    db.session.execute(sql, {"course_id":course_id, "course_name":course_name, \
                             "student_username":student_username, "teacher_username":teacher_username})
    db.session.commit()
    return