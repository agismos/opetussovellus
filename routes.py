from app import app
from flask import redirect, render_template, request, session
from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import users, courses

@app.route("/")
def index():
    all = courses.list_courses()

    generate_course = ""
    if users.check_status():
        generate_course = "<a href='/generate_course'>Lisää kurssi</a>"

    return render_template("index.html", courses=all, generate_course=generate_course)

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    if users.login(username, password, role):
        return redirect("/")
    else:
        message1 = "Virheellinen käyttäjätunnus tai salasana"
        return render_template("index.html", message1=message1)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/create_account")
def create_account():
    return render_template("create_account.html")

@app.route("/add_student", methods=["POST"])
def add_student():

    # Tee tarkistuksista funktiot tiedostoon users.py?

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    role = request.form["role"]
    error = "Virheellinen avain"
    value1 = "value=" + firstname
    value2 = "value=" + lastname
    value3 = "value=" + username
    value4 = "value=" + password1
    value5 = "value=" + password2

    if role == "teachers":
        if request.form["secretkey"] != "abc123":
            return render_template("create_account.html", error=error,
                                                        value1=value1,
                                                        value2=value2,
                                                        value3=value3,
                                                        value4=value4,
                                                        value5=value5)
        
    if users.check_username(username, role):
        if password1 != password2:
            password_check = "Salasanat eivät täsmää"
            return render_template("create_account.html", password_check=password_check,
                                                        value1=value1,
                                                        value2=value2,
                                                        value3=value3,
                                                        value4=value4,
                                                        value5=value5)

        realname = request.form["firstname"]
        realname += " " + request.form["lastname"]
        password = generate_password_hash(password1)
        users.register(username, realname, password, role)
        return redirect("/")
    
    else:
        message = "Käyttäjätunnus on varattu"

        return render_template("create_account.html", message=message,
                                                        value1=value1,
                                                        value2=value2,
                                                        value3=value3,
                                                        value4=value4,
                                                        value5=value5)
    
@app.route("/show_course_details/<course>")
def show_course_details(course):
    result = courses.course_information(course)
    allcourses = courses.list_courses()

    generate_course = ""
    if users.check_status():
        generate_course = "<a href='/generate_course'>Lisää kurssi</a>"

    hyperlink = ""
    if not users.check_status():
        hyperlink = f"<form action='/enroll' method='POST'> \
                    <input type='hidden' name='{course}'> \
                    <input type='submit' value='Ilmoittaudu kurssille'> \
                    </form>"
    
    return render_template("index.html", course_information=result, courses=allcourses, hyperlink=hyperlink,
                           generate_course=generate_course)


@app.route("/enroll", methods=["POST"])
def enroll():
    course_name = list(request.form.keys())[0]

    course_information= "Ilmoittautuminen lisätty. Tervetuloa kurssille!"

    if not courses.add_enrollment(course_name):
        course_information = "Olet jo ilmoittautunut tälle kurssille."

    all = courses.list_courses()
    return render_template("index.html", courses=all, course_information=course_information)

@app.route("/information")
def information():
    username = session["username"]
    role = "Opiskelija"
    column = "student_username"
    if users.check_status():
        role = "Opettaja"
        column = "teacher_username"
    
    my_courses = courses.my_courses(username, column)

    my_information = f"<h1>Omat tiedot</h1> \
                            <p>Käyttäjätunnus: {username} </p> \
                            <p>Status: {role} </p> \
                            Omat kurssit: {my_courses}"

    all = courses.list_courses()

    generate_course = ""
    if users.check_status():
        generate_course = "<a href='/generate_course'>Lisää kurssi</a>"

    return render_template("index.html", generate_course=generate_course,
                                courses=all, username=username, my_information=my_information)

@app.route("/generate_course")
def generate_course():
    return render_template("generate_course.html")

@app.route("/generate_course/add", methods=["POST"])
def generate_course_add():
    course_name = request.form["course_name"]
    credits = request.form["credits"]
    contents = request.form["contents"]
    courses.add_course(course_name, credits, contents)
    return redirect("/")