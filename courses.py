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
    sql = text(f"SELECT details FROM courses WHERE course_name='{course_name}'")
    db.session.execute(text("SET client_encoding TO 'UTF8';"))
    result = db.session.execute(sql)
    details = result.fetchone()
    print(details)
    return details[0]