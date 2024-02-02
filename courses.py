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

def add_enrollment(course_name):
    student_username = session['username']

    sql = text(f"SELECT * FROM enrollments WHERE course_name='{course_name}' AND \
               student_username='{student_username}'")
    result = db.session.execute(sql).fetchone()
    if result:
        return False

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
    return True

def my_courses(username, column):
    sql = text(f"SELECT course_name FROM enrollments WHERE {column}='{username}'")
    result = db.session.execute(sql)

    courses = result.fetchall()

    result = "<br>"

    for course in courses:
        result += str(course.course_name) + "<br>"

    return result

def add_course(course_name, credits, contents):

    teacher_name = session["username"]

    sql = text(f"SELECT (realname) FROM teachers WHERE username='{teacher_name}'")
    realname = db.session.execute(sql).fetchone()

    realname = realname.realname

    sql = text("INSERT INTO courses (course_name, credits, contents, \
               teacher_name, teacher_username) VALUES (:course_name, \
               :credits, :contents, :teacher_name, :teacher_username)")
    
    db.session.execute(sql, {"course_name":course_name, "credits":credits, \
                             "contents":contents, "teacher_name":realname, \
                                "teacher_username":teacher_name})
    db.session.commit()
    return

def add_to_table(course_name, question, answer, is_correct):
    sql = text(f"SELECT courses.id FROM courses WHERE courses.course_name='{course_name}'")
    id = db.session.execute(sql).fetchone()
    id = id[0]

    sql = text("INSERT INTO questions (course_id, course_name, question, answer, is_correct) \
               VALUES (:course_id, :course_name, :question, :answer, :is_correct)")
    
    db.session.execute(sql, {"course_id":id, "course_name":course_name, "question":question, \
                             "answer":answer, "is_correct":is_correct})
    
    db.session.commit()
    return