from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(username, password, role):
    sql = text(f"SELECT id, password FROM {role} WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            if role == "teacher":
                session["user_rights"] = "admin"
            return True
        else:
            return False

def check_username(username, rights):
    try:
        sql = text("INSERT INTO usernames (username, rights) VALUES (:username, :rights)")
        db.session.execute(sql, {"username":username, "rights":rights})
        db.session.commit()
    except:
        return False
    return True

def register(username, realname, password, role):
    sql = text(f"INSERT INTO {role} (realname, username, password) VALUES (:realname, " \
            ":username, :password) RETURNING id")
    db.session.execute(sql, {"realname":realname, "username":username, "password":password})
    db.session.commit()
    return

def check_status():
    try:
        username = session['username']
        sql = text(f"SELECT rights FROM usernames WHERE username='{username}'")
        status = db.session.execute(sql).fetchone()[0]
    except:
        return False

    if status == "teachers":
        return True
    return False