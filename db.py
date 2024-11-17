# Database connection: getters and setters

import sqlite3
from app import get_db
import time
from datetime import datetime
from random import choice
from string import ascii_lowercase, digits

def get_temp(what:str, table:str, cond_a:str, cond_b:any) -> list:
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
    Template to update specific data from the database

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

    username: the player’s username

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

def get_game(gameid:int) -> list:
    """
    Function to pull all the data related to a game from the databse

    gameid: the game's id

    Returns a list of all the data in the format 
        (gameid:int, p1:int, p2:int, p3:int, p4:int, over:bool)
    """
    return get_temp("*", "Games", "gameid", gameid)

def get_history(gameid:int) -> list:
    """
    Function to pull all played moves from a game from the database

    gameid: the game's id

    Returns all the moves of the game as a list of
        (gameid:int, movenumber:int, colour:int, piece:int, x:int, y:int, angle:int)
    """
    c = get_db().cursor()
    c.execute("SELECT * FROM Moves WHERE gameid = (?) ORDER BY movenumber ASC;", (gameid,))
    return c.fetchall()

def new_move(gameid:int, movenumber:int, colour:int, piece:int, x:int, y:int, angle:int) -> None:
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
    c.execute("INSERT INTO Moves VALUES ((?), (?), (?), (?));", (gameid, movenumber, colour, piece, x, y, angle))
    get_db().commit()

# We have yet to decide whether two users can have the same username
def new_player(username:str, password:str) -> bool:
    """
    Function to store a new user in the database if they don't already exist

    username: the new player's username
    password: the new player's password

    Returns whether the account was successfully created
    """
    c = get_db().cursor()
    pid = (c.execute("SELECT MAX(pid) FROM Players").fetchone()[0] or 0) + 1
    token = 2
    token_duration = 4 # in days
    token_expiration = time.time() + token_duration*24*60*60
    encrypted_pw = password

    c.execute("INSERT INTO Players VALUES ((?), (?), (?), (?), (?));", (pid, username, encrypted_pw, token, token_expiration))
    get_db().commit()
    return True

# We have yet to decide whether two users can have the same username
def update_username(pid:int, username:str) -> bool:
    """
    Function to change the username of a player

    pid: the player's id
    username: the new username

    Returns whether the change of username was successfull
    """
    set_temp("Players", "pid", username, "pid", pid)


def update_password(pid:int, password:str) -> None:
    """
    Function to modify the password of a player

    pid: the player's id
    password: the new password
    """
    set_temp("Players", "password", password, "pid", pid)

def new_game(p1:int, p2:int, p3:int, p4:int) -> None:
    """
    Function to create a new game with the players's ids

    p1: the first player's id (can be None)
    p2: the second player's id (can be None)
    p3: the third player's id (can be None)
    p4: the fourth player's id (can be None)
    """
    c = get_db().cursor()
    chars = ascii_lowercase + digits
    gameid = ''.join(choice(chars) for i in range(6))
    while get_temp("*", "Games", "gameid", gameid):
        gameid = ''.join(choice(chars) for i in range(6))

    c.execute("INSERT INTO Games VALUES ((?), (?), (?), (?), (?), (?));", (gameid, p1, p2, p3, p4, False))
    
    get_db().commit()

def end_game(gameid:int) -> None:
    """
    Function to end a game

    gameid: the id of the game to end
    """
    set_temp("Games", "over", True, "gameid", gameid)

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