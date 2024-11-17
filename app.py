from flask import Flask, request, abort, redirect, url_for, render_template, g, flash
import sqlite3
import random
import time
import os

app = Flask(__name__)
app.secret_key = b',DTuzn=#c9"F.)_'
##from db import new_player

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
    
    return render_template("index.html", time=time.localtime()[5])

@app.route("/signup", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        print(request.form)
        if(request.form["password"]==request.form["confirmation"]):
            res = new_player(request.form["username"], request.form["password"])
            #res = "e25102u", "azerty"
            if(res):
                pid, token = res
                return redirect(f"/?token={token}")
            else:
                flash("Ce pseudo est déjà pris !")
                return render_template("signup.html")
        
        else:
            flash("Les deux mots de passe ne correspondent pas…")
            return render_template("signup.html")