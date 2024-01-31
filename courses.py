from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def list_courses():
    sql = text("SELECT course_name FROM courses")
    result = db.session.execute(sql)
    courses = result.fetchall()
    print(courses)
    result = ""
    for course in courses:
        result += "<a href='/show_course_details'>" + f"{course[0]}" + "</a><br>"
    return result

def fetch_information():
    sql = text("SE")