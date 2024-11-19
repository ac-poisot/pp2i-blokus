from flask import Flask, request, abort, redirect, url_for, render_template, g, flash, make_response
import sqlite3
import random
import time
import os
from hashlib import sha512

app = Flask(__name__)
app.secret_key = b',DTuzn=#c9"F.)_'

# DB connection

DATABASE = 'blokus.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    c = get_db().cursor() # create the file

    if os.path.getsize(DATABASE) == 0:
        with open("scheme.txt", 'r') as file:
                sql_file = file.read()
        sql_commands = sql_file.split(';')
        for command in sql_commands:
            c.execute(command)
        get_db().commit()
    else:
        print("Database already exists. Skipping initialisation.")

from db import *

def wrap(template):
    if(request.cookies.get('exptoken') and float(request.cookies.get('exptoken')) > time.time()):
        pid = request.cookies.get('pid')
    else:
        pid = -1
    #print("pid: ", pid, float(request.cookies.get('exptoken')) > time.time(), float(request.cookies.get('exptoken')), time.time())
    return render_template("header.html", pid=pid) + template + render_template("footer.html")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    init_db()
    # p1 = new_player("Bouthier", "a")
    # p2 = new_player("Heurtel", "b")
    # p3 = new_player("Festor", "c")
    # p4 = new_player("Heudiard", "d")
    # g = new_game(p1, p2, p3, p4)
    # new_move(g, 2, 2, 5, 1, 1, 3)
    # new_move(g, 1, 1, 5, 4, 5, 3)
    # end_game(g)
    # update_username(p1, "Korkoro")
    # print(get_game(g))
    # print(get_history(g))
    # print(get_game_history(p3))
    
    return wrap(render_template("index.html", time=time.localtime()[5]))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return wrap(render_template("signup.html"))
    else:
        print(request.form)
        username = request.form["username"]
        password = request.form["password"]

        # check if the two passwords are the same
        if(password==request.form["confirmation"]):
            # check if one of the fields is empty
            if not username:
                flash("error_empty_username")
                return wrap(render_template("signup.html"))
            else:
                # check if the passwords meets the requirements
                if len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password) and any(char in ".,!:;?/%*#@{}[]$£€~^&|§<>" for char in password):
                    res = new_player(username, password)

                    # check if the username is too long
                    if len(username) <= 20:

                        # check if the username is already taken
                        if(res):
                            pid, token, exptoken = res

                            resp = make_response(redirect(f"/?token={token}"))
                            resp.set_cookie('pid', str(pid))
                            resp.set_cookie('token', token)
                            resp.set_cookie('exptoken', str(exptoken))

                            return resp
                    
                        else:
                            flash("error_username_taken")
                            return wrap(render_template("signup.html"))
                    else:
                        flash("error_username_length")
                        return wrap(render_template("signup.html"))
                else:
                    flash("error_requirements")
                    return wrap(render_template("signup.html"))
        
        else:
            flash("error_confirmation")
            return wrap(render_template("signup.html"))
        

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return wrap(render_template("login.html"))
    else:
        pid = get_pid(request.form["username"])
        if pid:
            password = request.form["password"].encode("utf-8")
            if(sha512(password).digest()==get_password(pid)):
                res = new_player(request.form["username"], request.form["password"])
                token, exptoken = update_token(pid)
                
                resp = make_response(redirect(f"/?token={token}"))
                resp.set_cookie('pid', str(pid))
                resp.set_cookie('token', token)
                resp.set_cookie('exptoken', str(exptoken))

                return resp
        
        
            else:
                flash("error_password")
                return wrap(render_template("login.html"))
        else:
            flash("error_username")
            return wrap(render_template("login.html"))
        

@app.route("/game")
def game():
    return wrap(render_template("game.html", grid=[[random.randint(0, 4) for j in range(20)] for i in range(20)]))

@app.route("/data")
def send_data():
    return [[random.randint(0, 4) for j in range(20)] for i in range(20)]

@app.route("/profile/<pid>")
def profile(pid):
    username = get_username(pid)
    nbvictories = 0
    nbdefeats = 0
    nbdraws = 0
    data = list(map(lambda elt: (elt[0], (elt[1], elt[2], elt[3], elt[4]), elt[5], elt[6]), get_game_history(pid)))
    states = []
    for i in range(len(data)):
        if(data[i][3] == 0):
            nbdraws += 1
            states.append("0")
        elif(data[i][3] == -1):
            states.append("?")
        elif(data[i][1][data[i][3]-1] == int(pid)):
            nbvictories += 1
            states.append("1")
        else:
            nbdefeats += 1
            states.append("-1")
    games=[{"date":data[i][2], "id":data[i][0], "state":states[i]} for i in range(len(data))]
    ratio = round(nbvictories/nbdefeats, 2) if nbdefeats != 0 else "?"
    return wrap(render_template("profile.html", username = username, nbvictories = nbvictories, nbdefeats = nbdefeats, nbdraws = nbdraws, ratio = ratio, games = games))