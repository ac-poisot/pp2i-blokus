from flask import Flask, request, abort, redirect, url_for, render_template, g
import sqlite3
import random
import time
app = Flask(__name__)


# DB connection

DATABASE = 'blokus.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    return render_template("index.html", time=time.localtime()[5])


@app.route("/data")
def send_data():
    print(time.localtime()[5])
    return {'token': request.args.get('token'), 'gameid':request.args.get('gameid'), 'time':time.localtime()[5]}