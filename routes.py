from app import app
from flask import redirect, render_template, request, session
from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import users

@app.route("/")
def index():
    return render_template("index.html")

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

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    role = request.form["role"]

    if users.check_username(username):
        realname = request.form["firstname"]
        realname += " " + request.form["lastname"]
        password = generate_password_hash(password1)
        users.register(username, realname, password, role)
        return redirect("/")
    
    else:
        message = "Käyttäjätunnus on varattu"
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        value1 = "value=" + firstname
        value2 = "value=" + lastname
        value3 = "value=" + username
        value4 = "value=" + password1
        value5 = "value=" + password2
        return render_template("create_account.html", message=message,
                                                        value1=value1,
                                                        value2=value2,
                                                        value3=value3,
                                                        value4=value4,
                                                        value5=value5)