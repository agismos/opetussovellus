from app import app
from flask import redirect, render_template, request, session
from db import db
from sqlalchemy.sql import text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/create_account")
def create_account():
    return render_template("create_account.html")

@app.route("/add_student", methods=["POST"])
def add_student():
    # Tämä antaa siis usernamen siinä muodossa kun se syötettiin lomakkeeseen: Tyyliin "Keijo"
    username = request.form["username"]


    #TEE TÄSTÄ OMA FUNKTIO:
    sql = text("SELECT * FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        message = "Käyttäjätunnus on varattu"
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
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
    
    realname = request.form["firstname"]
    realname += " " + request.form["lastname"]
    password = request.form["password1"]
    sql = text("INSERT INTO users (realname, username, password) VALUES (:realname, " \
               ":username, :password) RETURNING id")
    db.session.execute(sql, {"realname":realname, "username":username, "password":password})
    db.session.commit()
    return redirect("/")