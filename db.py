# Database connection: getters and setters

import sqlite3
from app import get_db
import time
from datetime import datetime
from random import choice
from string import ascii_lowercase, digits
from hashlib import sha512

# Constants

TOKEN_LENGTH = 6
GAMEID_LENGTH = 6
TOKEN_DURATION = 4 # in days

TOKEN_CHARS = ascii_lowercase + digits # Characters to use in tokens
GAMEID_CHARS = ascii_lowercase + digits # Characters to use in gameIDs

# Templates

def get_temp(what:str, table:str, cond_a:str, cond_b:any) -> list[tuple[any]]:
    """
    Template to pull specific data from the database

    what: the attribute(s) to select
    table: the table to search in
    cond_a: the condition attribute
    cond_b: the value the attribute should equal

    Returns the corresponding data as a list of tuples
    """
    c = get_db().cursor()
    a = c.execute(f"SELECT {what} FROM {table} WHERE {cond_a} = (?);", (cond_b,))
    return a.fetchall()

def set_temp(table:str, what:str, towhat:any, cond_a:str, cond_b:any) -> None:
    """
    Template to update a specific attribute from the database

    table: the table to search in
    what: the attribute to update
    towhat: the attribute's new value
    cond_a: the condition attribute
    cond_b: the value the attribute should equal

    Returns the corresponding data as a list of tuples
    """
    c = get_db().cursor()
    c.execute(f"UPDATE {table} SET {what} = (?) WHERE {cond_a} = (?);", (towhat, cond_b))
    get_db().commit()

# Getters & setters

def get_password(pid:int) -> str:
    """
    Function to pull the password of a player from the database

    pid: the player's id

    Returns the password
    """
    return get_temp("password", "Players", "pid", pid)[0][0]

def get_username(pid:int) -> str:
    """
    Function to pull the username of a player from the database

    pid: the player's id

    Returns the username
    """
    return get_temp("username", "Players", "pid", pid)[0][0]

def get_pid(username:str) -> int:
    """
    Function to pull the id of a player from the database

    username: the player's username

    Returns the id
    """
    return get_temp("pid", "Players", "username", username)[0][0]

def get_token(pid:int) -> str:
    """
    Function to pull the token of a player from the database

    pid: the player's id

    Returns the token if it has not expired, None if it has
    """
    exp_date = get_temp("tokenexpiration", "Players", "pid", pid)
    if time.time() > exp_date:
        return None
    else:
        return get_temp("token", "Players", "pid", pid)[0][0]

def get_game_history(pid:int) -> list[str]:
    """
    Function to pull all the games that a specific player has participated in

    pid: the player'id

    Returns a list of all the ids of games the player has participated in
    """
    c = get_db().cursor()
    c.execute("SELECT * FROM Games WHERE over = True AND (p1 = (?) OR p2 = (?) OR p3 = (?) OR p4 = (?)) ORDER BY start_time ASC;", (pid,)*4)
    return [i[0] for i in c.fetchall()]

def get_game(gameid:str) -> tuple:
    """
    Function to pull all the data related to a game from the databse

    gameid: the game's id

    Returns a list of all the data in the format 
        (gameid:str, p1:int, p2:int, p3:int, p4:int, start_time:float, over:bool, winner:int)
    """
    return get_temp("*", "Games", "gameid", gameid)[0]

def get_history(gameid:str) -> list[tuple]:
    """
    Function to pull all played moves from a game from the database

    gameid: the game's id

    Returns all the moves of the game sorted by number as a list of
        (movenumber:int, colour:int, piece:int, x:int, y:int, angle:int)
    """
    c = get_db().cursor()

    c.execute("SELECT * FROM Moves WHERE gameid = (?) ORDER BY movenumber ASC;", (gameid,))
    return [move[1:] for move in c.fetchall()]

def new_move(gameid:str, movenumber:int, colour:int, piece:int, x:int, y:int, angle:int) -> None:
    """
    Function to push a specific move to the database

    gameid: the game's id
    movenumber: which move it is (number since the beginning of the game)
    colour: the player that placed the piece
    piece: the number of the piece
    x: the piece's first coordinate
    y: the piece's second coordinate
    angle: the orientation of the piece [TODO what kind of int do we want]
    """
    c = get_db().cursor()
    c.execute("INSERT INTO Moves VALUES ((?), (?), (?), (?), (?), (?), (?));", (gameid, movenumber, colour, piece, x, y, angle))
    get_db().commit()

def new_player(username:str, password:str) -> any:
    """
    Function to store a new user in the database if they don't already exist

    username: the new player's username
    password: the new player's password

    Returns the id of the newly created player, False if username is already taken
    """
    if get_temp("*", "Players", "username", username):
        return False
    
    c = get_db().cursor()
    
    pid = (c.execute("SELECT MAX(pid) FROM Players").fetchone()[0] or 0) + 1

    token = ''.join(choice(TOKEN_CHARS) for i in range(TOKEN_LENGTH))
    while get_temp("*", "Players", "token", token):
        token = ''.join(choice(TOKEN_CHARS) for i in range(TOKEN_LENGTH))

    token_expiration = time.time() + TOKEN_DURATION*24*60*60
    encrypted_pw = sha512(password.encode("utf-8")).digest()

    c.execute("INSERT INTO Players VALUES ((?), (?), (?), (?), (?));", (pid, username, encrypted_pw, token, token_expiration))
    get_db().commit()
    return pid, token

def update_username(pid:int, username:str) -> bool:
    """
    Function to change the username of a player

    pid: the player's id
    username: the new username

    Returns whether the change of username was successful
    """
    if get_temp("*", "Players", "username", username):
        return False

    set_temp("Players", "username", username, "pid", pid)
    return True

def update_password(pid:int, password:str) -> None:
    """
    Function to modify the password of a player

    pid: the player's id
    password: the new password
    """
    set_temp("Players", "password", password, "pid", pid)

def update_token(pid:int) -> str:
    """
    Function to renew the token of a player

    pid: the player's id

    Returns the new token
    """
    token = ''.join(choice(TOKEN_CHARS) for i in range(TOKEN_LENGTH))
    while get_temp("*", "Players", "token", token):
        token = ''.join(choice(TOKEN_CHARS) for i in range(TOKEN_LENGTH))

    token_expiration = time.time() + TOKEN_DURATION*24*60*60

    set_temp("Players", "token", token, "pid", pid)
    set_temp("Players", "tokenexpiration", token_expiration, "pid", pid)
    return token

def new_game(p1:int, p2:int, p3:int, p4:int) -> str:
    """
    Function to create a new game with the players's ids

    p1: the first player's id (can be None)
    p2: the second player's id (can be None)
    p3: the third player's id (can be None)
    p4: the fourth player's id (can be None)

    Returns the id of the newly created game
    """
    c = get_db().cursor()

    gameid = ''.join(choice(GAMEID_CHARS) for i in range(GAMEID_LENGTH))
    while get_temp("*", "Games", "gameid", gameid):
        gameid = ''.join(choice(GAMEID_CHARS) for i in range(GAMEID_LENGTH))

    c.execute("INSERT INTO Games VALUES ((?), (?), (?), (?), (?), (?), (?), (?));", (gameid, p1, p2, p3, p4, time.time(), False, None)) 
    get_db().commit()
    return gameid

def end_game(gameid:str, winner:int) -> None:
    """
    Function to end a game

    gameid: the id of the game to end
    winner: the id of the winner of the game, congrats to them!
    """
    set_temp("Games", "over", True, "gameid", gameid)
    set_temp("Games", "over", True, "winner", winner)

def delete_player(pid:int):
    """
    Function to remove a player from the database
    Note: only the username and password of the player are removed

    pid: the id of the player to delete 
    """
    set_temp("Players", "username", "NULL", "pid", pid)
    set_temp("Players", "password", "NULL", "pid", pid)
    set_temp("Players", "token", "NULL", "pid", pid)
    set_temp("Players", "tokenexpiration", "NULL", "pid", pid)