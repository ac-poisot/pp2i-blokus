from flask import Flask, request, abort, redirect, url_for, render_template, g, flash, make_response, jsonify, session
import sqlite3
import time
from datetime import datetime
import os
from hashlib import sha512

app = Flask(__name__)
app.secret_key = b',DTuzn=#c9"F.)_'

# Constants

MAX_USERNAME_LENGTH = 14
MIN_PASSWORD_LENGTH = 8
SPECIAL_CHARS = ".,!:;?/%*#@{}[]$£€~^&|§<>"

# Only display errors and criticals 

import flask.cli    
flask.cli.show_server_banner = lambda *args: None

import logging
logging.getLogger("werkzeug").disabled = True


from pieces import pieces

# DB connection

DATABASE = 'blokus.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    c = get_db().cursor() # Create the file

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
from game import *
import ai

def createRoom(pid):
    roomid = new_game(pid, None, None, None, False)
    return roomid

def recreateGame(gameid):
    playerlist = get_playername_list(gameid)
    game = retrieve_game(4, get_history(gameid))
    for i in range(4):
        if playerlist[i] == None or playerlist[i] == "Empty slot":
            game.delete_player(i+1)

    if game.players:
        game.is_playing_index = game.is_playing_index % len(game.players)
        game.is_playing = game.players[game.is_playing_index]
    return game


def wrap(template, responsive=True):
    if(request.cookies.get('exptoken') and float(request.cookies.get('exptoken')) > time.time() and request.cookies.get('pid') and request.cookies.get('token') and request.cookies.get('token') == get_token(request.cookies.get('pid'))):
        pid = request.cookies.get('pid')
    else:
        pid = -1
    if responsive:
        return render_template("widgets/header.html", pid=pid) + template + render_template('widgets/background.html', pieces=pieces) + render_template("widgets/footer.html")
    else:
        return render_template("widgets/header.html", pid=pid) + template + render_template('widgets/background.html', pieces=pieces) + render_template("widgets/not_available.html") + render_template("widgets/footer.html")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


gameList = {}

@app.route("/")
def home():
    init_db()
    if(request.cookies.get('exptoken') and float(request.cookies.get('exptoken')) > time.time() and request.cookies.get('pid') and request.cookies.get('token') and request.cookies.get('token') == get_token(request.cookies.get('pid'))):
        pid = request.cookies.get('pid')
    else:
        pid = -1
    return wrap(render_template("pages/index.html", pid=pid))

@app.route("/rules")
def rules():
    return wrap(render_template("pages/rules.html", pieces=pieces))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if not(request.cookies.get('exptoken') and float(request.cookies.get('exptoken')) > time.time() and (request.cookies.get('pid') and request.cookies.get('token') and request.cookies.get('token') == get_token(request.cookies.get('pid')))):
            return wrap(render_template("pages/signup.html"))
        else:
            flash("already_logged_in")
            return wrap(render_template("pages/error.html"))
    else:
        username = request.form["username"]
        password = request.form["password"]

        # Check different requirements
        valid = True
        if(password != request.form["confirmation"]):
            valid = False
            flash("error_confirmation")
        if(not username):
            valid = False
            flash("error_empty_username")
        if ' ' in username:
            valid = False
            flash("error_space")
        if len(password) < MIN_PASSWORD_LENGTH or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password) or not any(char in SPECIAL_CHARS for char in password):
            valid = False
            flash("error_requirements")
        if len(username) > MAX_USERNAME_LENGTH:
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
            return wrap(render_template("pages/signup.html"))
        

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not(request.cookies.get('exptoken') and float(request.cookies.get('exptoken')) > time.time() and (request.cookies.get('pid') and request.cookies.get('token') and request.cookies.get('token') == get_token(request.cookies.get('pid')))):
            return wrap(render_template("pages/login.html"))
        else:
            flash("already_logged_in")
            return wrap(render_template("pages/error.html"))
    else:
        pid = get_pid(request.form["username"])
        if request.form["username"] and pid:
            password = request.form["password"].encode("utf-8")

            # If the password matches
            if(sha512(password).digest() == get_password(pid)):
                res = new_player(request.form["username"], request.form["password"])
                token, exptoken = update_token(pid)
                
                resp = make_response(redirect("/"))
                resp.set_cookie('pid', str(pid))
                resp.set_cookie('token', token)
                resp.set_cookie('exptoken', str(exptoken))

                return resp
        
        
            else:
                flash("error_password")
                return wrap(render_template("pages/login.html"))
        else:
            flash("error_username")
            return wrap(render_template("pages/login.html"))
        
@app.route("/games")
def games():
    pid = request.cookies.get("pid")
    if(not pid): # If not connected
        flash("error_not_connected")
        return wrap(render_template("pages/error.html"))

    pid = int(pid)
    if(not request.cookies.get("token") or get_token(pid) != request.cookies.get("token")): # If the token doesn’t exist, doesn’t match, or is outdated
        flash("error_not_connected")
        return wrap(render_template("pages/error.html"))

    data = list(map(lambda elt: (elt[0], (elt[1], elt[2], elt[3], elt[4]), elt[5], elt[6]), get_game_history(pid)))
    gameList = []
    roomList = []
    for i in range(len(data)):
        if(data[i][3] == -1):
            gameList.append({"date":str(datetime.fromtimestamp(data[i][2]))[:-7], "id":data[i][0].upper()})

        elif(data[i][3] == -2):
            roomList.append({"date":str(datetime.fromtimestamp(data[i][2]))[:-7], "id":data[i][0].upper()})
    return wrap(render_template("pages/games.html", games=gameList, rooms=roomList))

@app.route("/create")
def create_game():
    if(not request.cookies.get("pid")): # If not connected
        flash("error_not_connected")
        return wrap(render_template("pages/error.html"))
    
    pid = int(request.cookies.get("pid"))
    if(not request.cookies.get("token") or get_token(pid) != request.cookies.get("token")): # If the token doesn’t exist, doesn’t match, or is outdated
        flash("error_not_connected")
        return wrap(render_template("pages/error.html"))
    
    roomid = request.args.get("roomid")
    if(roomid == None):   # If no roomid is given, create a room
        roomid = createRoom(request.cookies.get("pid"))
        redirection = f"/create?roomid={roomid}"
        return redirect(redirection)
    
    elif (not get_room(roomid)): # If the roomid isn’t valid
        flash("non_existent_room")
        return wrap(render_template("pages/error.html"))
    
    players = get_room(roomid)
    if(pid in players): # If the player is part of the room
        return wrap(render_template("pages/create_game.html", roomid=roomid.upper(), master=players[0] == pid, players=get_playername_list(roomid), usernames=get_playername_list(roomid), ais=ai.aiNames), responsive=False)
    
    else: # Else, deny access
        flash("not_allowed")
        return wrap(render_template("pages/error.html"))
    
@app.route("/join")
def join():
    if(not request.cookies.get("pid")): # If not connected
        flash("error_not_connected")
        return wrap(render_template("pages/error.html"))
    pid = int(request.cookies.get("pid"))

    # If the token doesn’t exist, doesn’t match, or is outdated
    if(not request.cookies.get("token") or get_token(pid) != request.cookies.get("token")):
        flash("error_not_connected")
        return wrap(render_template("pages/error.html"))
    roomid = request.args.get("roomid")

    if(roomid == None): return redirect("/games") # If no roomid is given

    players = get_room(roomid)

    # If there are no players in the room (hence no room)
    if(not players):
        flash("non_existent_room")
        return wrap(render_template("pages/error.html"))
    
    # If the player is part of the room
    elif(pid in players):
        return redirect(f"/create?roomid={roomid}")
    
    # If they aren’t but a spot is available
    elif(-1 in players):
        players[players.index(-1)] = pid
        set_room(players, roomid)
        return redirect(f"/create?roomid={roomid}")
    # If they aren’t part of the room and the room is full
    else:
        flash("room_full")
        return wrap(render_template("pages/error.html"))

@app.route("/game")
def game():
    gameid = request.args.get("gameid").lower()
    if(not gameid): return redirect("/games") # If no gameid is given
    gameData = get_game(gameid)

    if(not gameData): return redirect("/games") # If no such game exists
    room = list(gameData)[1:5]
    pid = request.cookies.get("pid")

    if((not pid) or not request.cookies.get("token") or get_token(pid) != request.cookies.get("token")): # If not connected properly
        flash("error_not_connected")
        return wrap(render_template("pages/error.html"))
    
    if(not pid in room): # If the player isn’t in the list of players of the game
        flash("not_allowed")
        return wrap(render_template("pages/error.html"))
    
    if(gameData[6] == -2): return redirect(f"/create?roomid={gameid}") # If the game hasn’t been started yet

    if(not gameid in gameList.keys()): # If the game isn’t loaded by the server yet, do so with the database
        gameList[gameid] = recreateGame(gameid)
    game = gameList[gameid]

    # If no player can play (i.e. the game is finished), calculate and display the scoreboard
    if not game.players:
        scoreboard = []
        players = get_playername_list(gameid)
        for i in range(len(players)):
            if players[i] != None:
                scoreboard.append((players[i], game.score(i+1)))
        scoreboard.sort(reverse = True, key = lambda elt: elt[1])

        grid = [game.board[i][1:-1] for i in range(1, 21)]
        raw_history = get_history(gameid)[::-1]
        history = []
        for i in range(len(raw_history)):
            if(raw_history[i][3] == -1):
                history.append((players[raw_history[i][2]-1],))
            else:
                # Append the player, the piece as a matrix and its coordinates
                history.append((raw_history[i][2], players[raw_history[i][2]-1], rotate(raw_history[i][3], raw_history[i][6], raw_history[i][7]), (raw_history[i][4], raw_history[i][5])))

        return wrap(render_template("pages/scoreboard.html", scoreboard=scoreboard, grid=grid, history=history))
    
    grid = [game.board[i][1:-1] for i in range(1, 21)]
    players = get_playername_list(gameid)
    pieceList = [[pieces[elt-1] for elt in game.available[i]] for i in range(game.maxn)]
    piecesids = [[elt for elt in game.available[i]] for i in range(game.maxn)]
    scores = [0, 0, 0, 0]
    isplaying = game.players[game.is_playing_index]
    you = isplaying-1 if "Guest " in players[isplaying-1] and list(gameData)[1:5].index(str(pid)) == 0 else list(gameData)[1:5].index(str(pid))
    raw_history = get_history(gameid)[::-1]
    history = []
    for i in range(len(raw_history)):
        if(raw_history[i][3] == -1):
            history.append((players[raw_history[i][2]-1],))
        else:
            # Append the player, the piece as a matrix and its coordinates
            history.append((raw_history[i][2], players[raw_history[i][2]-1], rotate(raw_history[i][3], raw_history[i][6], raw_history[i][7]), (raw_history[i][4], raw_history[i][5])))

    return wrap(render_template("pages/game.html", grid=grid, players=players, pieces=pieceList, piecesids=piecesids, scores=scores, you=you, autoforfeit=gameData[7], history=history), responsive=False)


@app.route("/API/create", methods=['GET', 'POST'])
def players():
    roomid = request.args.get("roomid")
    if(not request.cookies.get("pid")): return jsonify({"error": "Not connected"}) # If not connected
    pid = int(request.cookies.get("pid"))
    if(not request.cookies.get("token") or get_token(pid) != request.cookies.get("token")): # If the token doesn’t exist, doesn’t match, or is outdated
        return jsonify({"error": "Not allowed"})
    if(not get_room(roomid)): return jsonify({"redirection": "/game"}) # If the room isn’t open, check if the game is open
    room = get_room(roomid)
    if pid in get_room(roomid): # If the player is part of the room
        if request.method == 'GET': # If it is just a GET request, allow it
            return jsonify({"players": get_room(roomid), "usernames": get_playername_list(roomid)})
        else: # If it is a POST request
            if("autoforfeit" in request.json.keys()):
                set_auto_forfeit(request.json["autoforfeit"], roomid)
                return jsonify({"players": get_room(roomid), "usernames": get_playername_list(roomid)})
            elif("players" in request.json.keys()): # If the request asks to change the player list
                players = request.json["players"] # Set the “players” list to the new list
                pindex = room.index(pid) # index of the player in the list of players

                if(get_game(roomid)[6] != -2): return jsonify({"error": "Non-existent room"}) # If the room isn’t open

                if(players[pindex] == -1 and pindex != 0): # If a player other than the game master leaves
                    room[pindex] = -1
                    set_room(room, roomid)
                    return jsonify({"redirection": "/"})
                
                # If the game master leaves
                elif(players[pindex] == -1 and pindex == 0):
                    delete_room(roomid)
                    return jsonify({"redirection": "/"})
                
                # If the player isn’t the game master, they aren’t allowed to use the next lines
                if(pindex != 0): return jsonify({"error": "Not allowed"})
                if "needAI" in request.json.keys(): # We create an AI if one is requested at a certain index
                    needAI = request.json["needAI"]
                    players[int(needAI['index'])] = f"AI {needAI['index']}-{int(needAI['level'])}"
                set_room(players, roomid)
                return jsonify({"players": get_room(roomid), "usernames": get_playername_list(roomid)})
            
            # If the game master requests to make a game from this room
            elif("launch" in request.json.keys() and room and room.index(pid) == 0):
                    set_room(list(map(lambda elt: elt if elt != -1 else None, get_room(roomid))), roomid)
                    change_game_state(roomid, -1)
                    return {"redirection": "/game"}
            else: return jsonify({"error": "Not allowed"})
    else:
        return jsonify({"error": "Not allowed"})

@app.route("/API/data", methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        if(not request.cookies.get("pid")): return jsonify({"error": "Not connected"}) # If not connected
        
        pid = int(request.cookies.get("pid"))
        token = request.cookies.get("token")
        if(not token or get_token(pid) != token): return jsonify({"error": "Not connected"}) # If the token doesn’t exist, doesn’t match, or is outdated

        gameid = request.args.get("gameid").lower()
        if(not gameid): return jsonify({"error": "Not allowed"}) # If no gameid is given

        gameData = get_game(gameid)

        # If such a game exists and the player is part of it
        if(gameData and (str(pid) == gameData[1] or str(pid) == gameData[2] or str(pid) == gameData[3] or str(pid) == gameData[4])):
            if(gameData[6] != -1): return jsonify({"error": "Not allowed"}) # If the game isn’t currently running
            if(not gameid in gameList.keys()): # If the game isn’t currently loaded by the server, load it from the database
                gameList[gameid] = recreateGame(gameid)
            game = gameList[gameid]
            grid = [game.board[i][1:-1] for i in range(1, 21)]
            players = get_playername_list(gameid)
            pieceList = [[pieces[elt-1] for elt in game.available[i]] for i in range(game.maxn)]
            piecesids = [[elt for elt in game.available[i]] for i in range(game.maxn)]
            scores = [0, 0, 0, 0]
            if not game.players: return jsonify({"finished": True})
            isplaying = game.players[game.is_playing_index]
            you = isplaying if "Guest " in players[isplaying-1] and list(gameData)[1:5].index(str(pid)) == 0 else list(gameData)[1:5].index(str(pid))+1

            raw_history = get_history(gameid)[::-1]
            history = []
            for i in range(len(raw_history)):
                if(raw_history[i][3] == -1):
                    history.append((players[raw_history[i][2]-1]))
                else:
                    # Append the player, the piece as a matrix and its coordinates
                    history.append((raw_history[i][2], players[raw_history[i][2]-1], rotate(raw_history[i][3], raw_history[i][6], raw_history[i][7]), (raw_history[i][4], raw_history[i][5])))


            return {
                "grid": grid,
                "players": players,
                "pieces": pieceList,
                "piecesids": piecesids,
                "scores": scores,
                "isplaying": isplaying,
                "you": you,
                "history": history
            }
        else:
            return jsonify({"error": "Not allowed"})
    else: # If it is a POST request
        data = request.json # We retrieve the data from the request
        if(not request.cookies.get("pid")): return jsonify({"error": "Not connected"}) # If not connected

        pid = int(request.cookies.get("pid"))
        token = request.cookies.get("token")
        if(not token or get_token(pid) != token): return jsonify({"error": "Not connected"}) # If the token doesn’t exist, doesn’t match, or is outdated

        gameid = request.args.get("gameid").lower()
        if(not gameid): return jsonify({"error": "Not allowed"}) # If no gameid is given

        gameData = get_game(gameid)

        # If the game exists and the player is part of it
        if(gameData and (str(pid) in list(gameData)[1:5])):
            if(not gameid in gameList.keys()): # If the game is not loaded yet, load it from the database
                gameList[gameid] = recreateGame(gameid) 
            game = gameList[gameid]
            pindex = list(gameData)[1:5].index(str(pid)) # Index of the player in the list of players
            # Check if it’s the player’s turn
            if str(pid) == gameData[game.players[game.is_playing_index]]:

                # If the player wishes to forfeit
                if "piece" not in data.keys():
                        new_move(gameid, game.is_playing, -1, 0, 0, 0, False) # Indicate forfeit
                        game.delete_player(game.is_playing)
                        if game.is_playing_index >= len(game.players):
                            game.is_playing_index = 0
                        if game.players:
                            game.is_playing = game.players[game.is_playing_index]  
                        while list(gameData)[1:5][game.is_playing-1][:3] == "AI " and game.players:
                            if(not game.can_play(game.is_playing)):
                                new_move(gameid, game.is_playing, -1, 0, 0, 0, False)
                                game.delete_player(game.is_playing)
                                if game.is_playing_index >= len(game.players):
                                    game.is_playing_index = 0
                                if game.players:
                                    game.is_playing = game.players[game.is_playing_index]
                            else:
                                ai.ais[int(list(gameData)[1:5][game.is_playing-1][-1])](gameid, game)
                                game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
                                if game.players: game.is_playing = game.players[game.is_playing_index]

                # If the move given can be made and it’s the player’s turn
                elif data['piece'] in game.available[pindex] and game.is_legal(data['piece'], data['orientation']*90, (data['y'], data['x']), data['inverted'], game.players[game.is_playing_index]): # (data['piece'], data['orientation']*90, data['inverted'], (data['x'], data['y'])) in game.possible_moves[game.is_playing_index]
                    game.add_piece(data['piece'], data['orientation']*90, (data['y'], data['x']), data['inverted']) # We play the move
                    new_move(gameid, pindex+1, int(data['piece']), data['y'], data['x'], data['orientation']*90, data['inverted'])

                    # We figure out who is the next player
                    game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
                    if game.players: game.is_playing = game.players[game.is_playing_index]

                    if gameData[7]: # If auto-forfeit is on
                        while ((not game.can_play(game.is_playing)) or list(gameData)[1:5][game.is_playing-1][:3] == "AI ") and game.players:
                            if(not game.can_play(game.is_playing)):
                                new_move(gameid, game.is_playing, -1, 0, 0, 0, False)
                                game.delete_player(game.is_playing)
                                if game.is_playing_index >= len(game.players):
                                    game.is_playing_index = 0
                                if game.players:
                                    game.is_playing = game.players[game.is_playing_index]
                            else:
                                ai.ais[int(list(gameData)[1:5][game.is_playing-1][-1])](gameid, game)
                                game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
                                if game.players: game.is_playing = game.players[game.is_playing_index]
                    else:
                        while list(gameData)[1:5][game.is_playing-1][:3] == "AI " and game.players:
                            if(not game.can_play(game.is_playing)):
                                new_move(gameid, game.is_playing, -1, 0, 0, 0, False)
                                game.delete_player(game.is_playing)
                                if game.is_playing_index >= len(game.players):
                                    game.is_playing_index = 0
                                if game.players:
                                    game.is_playing = game.players[game.is_playing_index]
                            else:
                                ai.ais[int(list(gameData)[1:5][game.is_playing-1][-1])](gameid, game)
                                game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
                                if game.players: game.is_playing = game.players[game.is_playing_index]



            # If it is a local player’s turn and the specified move can be played
            elif pindex == 0 and "Guest " in gameData[game.players[game.is_playing_index]]:
                # If the player wishes to forfeit
                if "piece" not in data.keys():
                    new_move(gameid, game.is_playing, -1, 0, 0, 0, False) # Indicate forfeit
                    game.delete_player(game.is_playing)
                    if game.is_playing_index >= len(game.players):
                        game.is_playing_index = 0
                    if game.players:
                        game.is_playing = game.players[game.is_playing_index]  
                    while list(gameData)[1:5][game.is_playing-1][:3] == "AI " and game.players:
                        if(not game.can_play(game.is_playing)):
                            new_move(gameid, game.is_playing, -1, 0, 0, 0, False)
                            game.delete_player(game.is_playing)
                            if game.is_playing_index >= len(game.players):
                                game.is_playing_index = 0
                            if game.players:
                                game.is_playing = game.players[game.is_playing_index]
                        else:
                            ai.ais[int(list(gameData)[1:5][game.is_playing-1][-1])](gameid, game)
                            game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
                            if game.players: game.is_playing = game.players[game.is_playing_index]
                
                elif data['piece'] in game.available[game.players[game.is_playing_index]-1] and game.is_legal(data['piece'], data['orientation']*90, (data['y'], data['x']), data['inverted'], game.players[game.is_playing_index]):
                    game.add_piece(data['piece'], data['orientation']*90, (data['y'], data['x']), data['inverted']) # We play the move
                    new_move(gameid, game.players[game.is_playing_index], int(data['piece']), data['y'], data['x'], data['orientation']*90, data['inverted'])

                    # We figure out who is the next player
                    game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
                    if game.players: game.is_playing = game.players[game.is_playing_index]

                    if gameData[7]: # If auto-forfeit is on
                        while ((not game.can_play(game.is_playing)) or list(gameData)[1:5][game.is_playing-1][:3] == "AI ") and game.players:
                            if(not game.can_play(game.is_playing)):
                                new_move(gameid, game.is_playing, -1, 0, 0, 0, False)
                                game.delete_player(game.is_playing)
                                if game.is_playing_index >= len(game.players):
                                    game.is_playing_index = 0
                                if game.players:
                                    game.is_playing = game.players[game.is_playing_index]
                            else:
                                ai.ais[int(list(gameData)[1:5][game.is_playing-1][-1])](gameid, game)
                                game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
                                if game.players: game.is_playing = game.players[game.is_playing_index]
                    else:
                        while list(gameData)[1:5][game.is_playing-1][:3] == "AI " and game.players:
                            if(not game.can_play(game.is_playing)):
                                new_move(gameid, game.is_playing, -1, 0, 0, 0, False)
                                game.delete_player(game.is_playing)
                                if game.is_playing_index >= len(game.players):
                                    game.is_playing_index = 0
                                if game.players:
                                    game.is_playing = game.players[game.is_playing_index]
                            else:
                                ai.ais[int(list(gameData)[1:5][game.is_playing-1][-1])](gameid, game)
                                game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
                                if game.players: game.is_playing = game.players[game.is_playing_index]


            grid = [game.board[i][1:-1] for i in range(1, 21)]
            players = get_playername_list(gameid)
            pieceList = [[pieces[elt-1] for elt in game.available[i]] for i in range(game.maxn)]
            piecesids = [[elt for elt in game.available[i]] for i in range(game.maxn)]
            scores = [0, 0, 0, 0]
            if not game.players:
                scoreboard = []
                for i in range(len(players)):
                    if players[i] != None:
                        scoreboard.append((i+1, game.score(i+1)))
                if(len(scoreboard) == 1):
                    state = 0
                else:
                    scoreboard.sort(reverse = True, key = lambda elt: elt[1])
                    if(scoreboard[0][1] != scoreboard[1][1]):
                        state = scoreboard[0][0]
                    else:
                        state = 0
                change_game_state(gameid, state)
                return jsonify({"finished": True})

            isplaying = game.players[game.is_playing_index]
            you = isplaying if "Guest " in players[isplaying-1] and list(gameData)[1:5].index(str(pid)) == 0 else list(gameData)[1:5].index(str(pid))+1

            raw_history = get_history(gameid)[::-1]
            history = []
            for i in range(len(raw_history)):
                if(raw_history[i][3] == -1):
                    history.append((players[raw_history[i][2]-1]))
                else:
                    # Append the player, the piece as a matrix and its coordinates
                    history.append((raw_history[i][2], players[raw_history[i][2]-1], rotate(raw_history[i][3], raw_history[i][6], raw_history[i][7]), (raw_history[i][4], raw_history[i][5])))

            return {
                "grid": grid,
                "players": players,
                "pieces": pieceList,
                "piecesids": piecesids,
                "scores": scores,
                "isplaying": isplaying,
                "you": you,
                "history": history
            }
        else:
            return jsonify({"error": "Not allowed"})

@app.route("/change_username", methods=['GET', 'POST'])
def change_username():
    if request.method == 'GET':
        pid = request.cookies.get('pid')
        if((not pid) or not request.cookies.get("token") or get_token(int(pid)) != request.cookies.get("token")): # If the player isn’t connected properly
            flash("error_not_connected")
            return wrap(render_template("pages/error.html"))
        return wrap(render_template("pages/change_username.html"))
    else:
        pid = request.cookies.get('pid')
        if((not pid) or not request.cookies.get("token") or get_token(int(pid)) != request.cookies.get("token")): # If the player isn’t connected properly
            flash("error_not_connected")
            return wrap(render_template("pages/error.html"))
        if request.form["username"]:
            password = request.form["password"].encode("utf-8")
            if(sha512(password).digest() == get_password(pid)):
                if not update_username(pid , request.form["username"]):
                    flash("error_username_taken")
                    return wrap(render_template("pages/change_username.html"))
                    
                resp = make_response(redirect(f"/profile/{pid}"))
                return resp
        
        
            else:
                flash("error_password")
                return wrap(render_template("pages/change_username.html"))
        else:
            flash("error_empty_username")
            return wrap(render_template("pages/change_username.html"))

@app.route("/credits", methods=['GET', 'POST'])
def credit():
    return wrap(render_template('pages/credits.html'))

@app.route("/profile/<pid>", methods=['GET', 'POST'])
def profile(pid):
    if request.method == 'GET':
        vpid = request.cookies.get('pid')
        if((not vpid) or not request.cookies.get("token") or get_token(int(vpid)) != request.cookies.get("token")): # If the visitor isn’t connected properly
            vis_username = None
        else:
            vis_username = get_username(request.cookies.get('pid'))

        username = get_username(pid)
        if username and username != "410 deleted":
            nbvictories = 0
            nbdefeats = 0
            nbdraws = 0
            data = list(map(lambda elt: (elt[0], (elt[1], elt[2], elt[3], elt[4]), elt[5], elt[6]), get_game_history(pid)))
            data = list(filter(lambda elt: elt[3] >= 0, data))
            states = []
            for i in range(len(data)):
                if(data[i][3] == 0):
                    nbdraws += 1
                    states.append("0")
                elif(data[i][1][data[i][3]-1] == pid):
                    nbvictories += 1
                    states.append("1")
                else:
                    nbdefeats += 1
                    states.append("-1")
            games = [{"date":str(datetime.fromtimestamp(data[i][2]))[:-7], "id":data[i][0].upper(), "state":states[i]} for i in range(len(data))]
            ratio = round(nbvictories/nbdefeats, 2) if nbdefeats != 0 else "?"
            return wrap(render_template("pages/profile.html", username = username, nbvictories = nbvictories, nbdefeats = nbdefeats, nbdraws = nbdraws, ratio = ratio, games = reversed(games), vis_username=vis_username))
        else:
            if username:
                flash("deleted_user")
                return wrap(render_template("pages/error.html"))
            else:
                flash("non_existent_user")
                return wrap(render_template("pages/error.html"))
    else:
        
        delete_player(pid)
        return make_response(redirect("/"))

    
@app.errorhandler(404)
def page_not_found(e):
    flash("404")
    return wrap(render_template('pages/error.html'))

@app.route("/creditss", methods=['GET', 'POST'])
def credits():
    return wrap(render_template('pages/creditss.html'))