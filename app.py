from flask import Flask, request, abort, redirect, url_for, render_template, g
import sqlite3
import random
import time
import os
app = Flask(__name__)

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
    return render_template("index.html", time=time.localtime()[5])


@app.route("/data")
def send_data():
    print(time.localtime()[5])
    return {'token': request.args.get('token'), 'gameid':request.args.get('gameid'), 'time':time.localtime()[5]}