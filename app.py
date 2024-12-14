from flask import Flask, request, abort, redirect, url_for, render_template, g, flash, make_response, jsonify, session
import sqlite3
import random
import time
import os
from hashlib import sha512

app = Flask(__name__)
app.secret_key = b',DTuzn=#c9"F.)_'

## Only display errors and criticals 

import flask.cli    
flask.cli.show_server_banner = lambda *args: None

import logging
logging.getLogger("werkzeug").disabled = True



from game import p_tempo

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

def createRoom(pid):
    roomid = new_game(pid, None, None, None)
    return roomid


def wrap(template):
    if(request.cookies.get('exptoken') and float(request.cookies.get('exptoken')) > time.time()):
        pid = request.cookies.get('pid')
    else:
        pid =-1
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
        if not(request.cookies.get('exptoken') and float(request.cookies.get('exptoken')) > time.time()):
            return wrap(render_template("signup.html"))
        else:
            flash("already_logged_in")
            return wrap(render_template("404.html"))
    else:
        username = request.form["username"]
        password = request.form["password"]

        # check different requirements
        valid = True
        if(password!=request.form["confirmation"]):
            valid = False
            flash("error_confirmation")
        if(not username):
            valid = False
            flash("error_empty_username")
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password) or not any(char in ".,!:;?/%*#@{}[]$£€~^&|§<>" for char in password):
            valid = False
            flash("error_requirements")
        if len(username) > 20:
            valid = False
            flash("error_username_length")
        if (username and get_pid(username)) or username == "DELETED":
            valid = False
            flash("error_username_taken")
        
        if valid:
            res = new_player(username, password)
            pid, token, exptoken = res

            resp = make_response(redirect(f"/?token={token}"))
            resp.set_cookie('pid', str(pid))
            resp.set_cookie('token', token)
            resp.set_cookie('exptoken', str(exptoken))

            return resp
                    
        else:
            return wrap(render_template("signup.html"))
        

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not(request.cookies.get('exptoken') and float(request.cookies.get('exptoken')) > time.time()):
            return wrap(render_template("login.html"))
        else:
            flash("alread_logged_in")
            return wrap(render_template("404.html"))
    else:
        pid = get_pid(request.form["username"])
        if request.form["username"] and pid:
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
        
@app.route("/not_connected")
def not_connected():
    return wrap(render_template("not_connected.html"))

@app.route("/not_allowed")
def not_allowed():
    return wrap(render_template("not_allowed.html"))

@app.route("/non_existent_room")
def non_existent_room():
    return wrap(render_template("non_existent_room.html"))

@app.route("/room_full")
def game_full():
    return wrap(render_template("room_full.html"))
        
@app.route("/games")
def games():
    return wrap(render_template("games.html"))

@app.route("/create")
def create_game():
    if(not request.cookies.get("pid")): return redirect("/not_connected")
    pid = int(request.cookies.get("pid"))
    if(get_token(pid) != request.cookies.get("token")): return redirect("/not_connected")
    roomid = request.args.get("roomid")
    if(roomid == None):
        roomid = createRoom(request.cookies.get("pid"))
        redirection = f"/create?roomid={roomid}"
        return redirect(redirection)
    elif (not get_room(roomid)):
        return redirect("/non_existent_room")
    players = get_room(roomid)
    if(pid in players):
        return wrap(render_template("create_game.html", roomid=roomid, master=players[0] == pid, players=get_playername_list(roomid), usernames=get_playername_list(roomid)))
    else:
        return redirect("/not_allowed")
    
@app.route("/join")
def join():
    if(not request.cookies.get("pid")): return redirect("/not_connected")
    pid = int(request.cookies.get("pid"))
    if(get_token(pid) != request.cookies.get("token")): return redirect("/not_connected")
    roomid = request.args.get("roomid")
    if(roomid == None):
        return redirect("/games")
    players = get_room(roomid)
    if(not players):
        return redirect("/non_existent_room")
    elif(pid in players):
        return wrap(render_template("create_game.html", rid=request.args.get("roomid"), master=True))
    elif(-1 in players):
        players[players.index(-1)] = pid
        set_room(players, roomid)
        return redirect(f"/create?roomid={roomid}")
    else:
        return redirect("/room_full")


@app.route("/game")
def game():
    return wrap(render_template("game.html", grid=[[random.randint(0, 4) for j in range(20)] for i in range(20)], players=["test", "test2", "test3", "test4"], pieces=[list(map(lambda elt: [elt[j] for j in range(len(elt))], p_tempo.values())) for i in range(4)], scores=[0, 0, 0, 0]))


@app.route("/API/players", methods=['GET', 'POST'])
def players():
    roomid = request.args.get("roomid")
    if(not request.cookies.get("pid")): return jsonify({"error": "Not connected"})
    pid = int(request.cookies.get("pid"))
    if(get_token(pid) != request.cookies.get("token")): return redirect("/not_connected")
    if(not get_room(roomid)): return jsonify({"error": "Non-existent room"})
    room = get_room(roomid)
    if pid in get_room(roomid) :
        if request.method == 'GET':
            return jsonify({"players": get_room(roomid), "usernames": get_playername_list(roomid)}) ## -1 pour un "poste" ouvert mais non pris et None pour un fermé
        else:
            players = request.json["players"]
            pindex = players[room.index(pid)]
            if(players[pindex] == -1 and pindex != 0):
                room[pindex] = -1
                set_room(room, roomid)
                return jsonify({"redirection": "/"})
            elif(players[pindex] == -1 and pindex == 0):
                delete_room(roomid)
                return jsonify({"redirection": "/"})
            if "needAI" in request.json.keys():
                needAI = request.json["needAI"]
                players[int(needAI['index'])] = f"AI{int(needAI['level'])}" ## TODO : add the AI
            if(get_room(roomid)[0] != pid): return jsonify({"error": "Not allowed"})
            set_room(players, roomid)
            return jsonify({"players": get_room(roomid), "usernames": get_playername_list(roomid)})
    else:
        return jsonify({"error": "Not allowed"})

@app.route("/data", methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        if(not request.cookies.get("pid")): return jsonify({"error": "Not connected"})
        pid = int(request.cookies.get("pid"))
        token = request.cookies.get("token")
        if(token and get_token(pid) != token): return redirect("/not_connected")
        gameData = get_game(request.args.get("gameid"))
        if(gameData and (pid == gameData[1] or pid == gameData[2] or pid == gameData[3] or pid == gameData[4])):
            return {
                "grid": [[random.randint(0, 4) for j in range(20)] for i in range(20)],
                "players": ["Test", "Test2", "Test3", "Test4"],
                "pieces": [list(map(lambda elt: [elt[j] for j in range(len(elt))], p_tempo.values())) for i in range(4)],
                "scores": [0, 0, 0, 0]
            }
        else:
            return jsonify({"error": "Not allowed"})
    else: ## VERIFICATION DE L'IDENTITE ET QUE C'EST SON TOUR NECESSAIRES
        data = request.json
        print(data)
        return jsonify("Move successfully played")

@app.route("/change_username", methods=['GET', 'POST'])
def change_username():
    if request.method == 'GET':
        if(request.cookies.get('exptoken') and float(request.cookies.get('exptoken')) > time.time()):
            return wrap(render_template("change_username.html"))
        else:
            flash("error_not_connected")
            return wrap(render_template("404.html"))
    else:
        pid = request.cookies.get('pid')
        if request.form["username"]:
            password = request.form["password"].encode("utf-8")
            if(sha512(password).digest()==get_password(pid)):
                if not update_username(pid , request.form["username"]):
                    flash("error_username_taken")
                    return wrap(render_template("change_username.html"))
                    
                resp = make_response(redirect(f"/profile/{pid}"))
                return resp
        
        
            else:
                flash("error_password")
                return wrap(render_template("change_username.html"))
        else:
            flash("error_empty_username")
            return wrap(render_template("change_username.html"))


@app.route("/profile/<pid>", methods=['GET', 'POST'])
def profile(pid):
    if request.method == 'GET':
        if(request.cookies.get('exptoken') and float(request.cookies.get('exptoken')) > time.time()):
            vis_username = get_username(request.cookies.get('pid'))
        else:
            vis_username = None
        username = get_username(pid)
        if username:
            if username == "DELETED":
                flash("user_deleted")
                return wrap(render_template("404.html"))
            else:
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
                return wrap(render_template("profile.html", username = username, nbvictories = nbvictories, nbdefeats = nbdefeats, nbdraws = nbdraws, ratio = ratio, games = games, vis_username=vis_username))
        else:
            flash("non_existent_user")
            return wrap(render_template("404.html"))
    else:
        
        delete_player(pid)
        return make_response(redirect("/"))

    
@app.errorhandler(404)
def page_not_found(e):
    flash("404")
    return wrap(render_template('404.html'))

@app.route("/credits", methods=['GET', 'POST'])
def credit():
    return wrap(render_template('credits.html'))