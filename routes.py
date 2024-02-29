from app import app
from flask import redirect, render_template, request, session
from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import users, courses
from os import getenv

@app.route("/")
def index():
    all = courses.list_courses()

    generate_course = ""
    if users.check_status():
        generate_course = "<a href='/generate_course'>Lisää tentti</a>"

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
        if request.form["secretkey"] != getenv("TEACHER_KEY"):
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
        generate_course = "<a href='/generate_course'>Lisää tentti</a>"

    hyperlink = ""
    if not users.check_status():
        hyperlink = f"<form action='/enroll' method='POST'> \
                    <input type='hidden' name='{course}'> \
                    <input type='submit' value='Ilmoittaudu tenttiin'> \
                    </form>"
    
    return render_template("index.html", course_information=result, courses=allcourses, hyperlink=hyperlink,
                           generate_course=generate_course)


@app.route("/enroll", methods=["POST"])
def enroll():
    course_name = list(request.form.keys())[0]

    course_information= "Ilmoittautuminen lisätty."

    if not courses.add_enrollment(course_name):
        course_information = "Olet jo ilmoittautunut tähän tenttiin."

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

    my_information = f"<h1>Käyttäjätiedot</h1> \
                            <p>Käyttäjätunnus: {username} </p> \
                            <p>Status: {role} </p> \
                            Omat tentit: {my_courses}"
    if users.check_status():
        my_information += "<a href='/edit_exam'>Siirry tentin muokkaukseen</a>"

    all = courses.list_courses()

    generate_course = ""
    if users.check_status():
        generate_course = "<a href='/generate_course'>Lisää tentti</a>"

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
    return redirect(f"/add_questions/{course_name}")

@app.route("/add_questions/<course_name>")
def add_question(course_name):
    information = f"<input type='hidden' name='{course_name}'>"
    return render_template("add_question.html", course_name=course_name,
                                                information=information)

@app.route("/add_answers", methods=["POST", "GET"])
def add_answers():
    course_name = request.form["course_name"]
    question = request.form["question"]

    return render_template("add_answer.html", course_name=course_name,
                                                question=question)

@app.route("/add_to_database", methods=["POST"])
def add_to_database():

    course_name = request.form["course_name"]
    question = request.form["question"]
    answer = request.form["answer"]
    trueorfalse = request.form["trueorfalse"]


    courses.add_to_table(course_name, question, answer, trueorfalse)

    return render_template("add_answer.html", course_name=course_name,
                                                question=question)

@app.route("/exams")
def exams():
    username = session["username"]
    my_courses = courses.list_my_courses(username)
    to_render = courses.render(my_courses)

    return render_template("exams.html", my_courses=to_render)

@app.route("/exams/download", methods=["POST"])
def exams_download():

    course = request.form["course"]

    questions = courses.fetch_questions(course)

    return render_template("download_exam.html", questions=questions)

@app.route("/answers", methods=["POST"])
def answers():

    username = session["username"]
    answers = []

    for key in request.form:
        answers.append(request.form[key])

    course = answers[0]

    answers = answers[1:]

    result = courses.check_answers(course, answers, username)

    points = result[0]
    max_points = result[1]

    
    return render_template("answers.html", points=points, max_points=max_points)

@app.route("/edit_exam")
def edit_exam():

    username = session["username"]

    result = courses.select_courses(username)

    return render_template("edit_exam.html", result=result)

@app.route("/edit_exam/<course>")
def edit(course):

    html = courses.list_questions(course)

    return render_template("list_all_questions.html", html=html, course=course)

@app.route("/remove_question/", methods=["POST"])
def remove_question():

    values = request.form.to_dict()

    information = []

    for value in values:
        information.append(value)

    courses.remove_question(information)

    html = courses.list_questions(information[1])

    return render_template("list_all_questions.html", html=html, course=information[1])