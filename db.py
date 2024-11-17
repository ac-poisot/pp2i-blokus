# Database connection: getters and setters

import sqlite3
from app import get_db
from time import time

def get_temp(what:str, table:str, cond_a:str, cond_b:any) -> list:
    """
    Template to get specific data from the database

    what: attributes we want
    table: the table to search in
    cond_a: the condition attribute
    cond_b: the condition the attribute must satisfy 

    Returns the corresponding data as a list of tuples
    """
    c = get_db().cursor()
    c.executemany("SELECT (?) FROM (?) WHERE (?) = (?);", [what, table, cond_a, cond_b])
    return c.fetchall()

def set_temp(table:str, what:str, towhat:any, cond_a:str, cond_b:any) -> None:
    """
    Template to get specific data from the database

    what: attributes we want
    table: the table to search in
    cond_a: the condition attribute
    cond_b: the condition the attribute must satisfy 

    Returns the corresponding data as a list of tuples
    """
    c = get_db().cursor()
    c.execute("UPDATE (?) SET (?) = (?) WHERE (?) = (?);", [table, what, cond_a, cond_b])
    get_db().commit()


def get_password(pid:str) -> int:
    """
    Function to get the password of a player from the db

    pid: player's id

    Returns the password
    """
    return get_temp("password", "Players", "pid", pid)

def get_token(pid:str) -> str:
    """
    Function to get the token of a player from the db

    pid: player's id

    Returns the token
    """
    exp_date = get_temp("tokenexpiration", "Players", "pid", pid)
    if time() > exp_date:
        return None
    else:
        return get_temp("token", "Players", "pid", pid)

def get_game(gameid:int) -> list:
    """
    Function to get every data stored for a specific game from the db

    gameid: game's id

    Returns a list of all data
    """
    return get_temp("*", "Games", "gameid", gameid)


def get_history(gameid:int) -> list:
    """
    Function to get all played moves from a game

    gameid: game's id

    Returns all the moves of the game
    """
    c = get_db().cursor()
    c.executemany("SELECT * FROM Moves WHERE gameid = (?) ORDER BY movenumber ASC;", [gameid])
    return c.fetchall()

def new_move(gameid:int, movenumber:int, colour:int, piece:int, x:int, y:int, angle:int) -> None:
    """
    Function to push a specific move to the db

    gameid: game's id
    movenumber: which move it is (number since the beginning of the game)
    colour: specify which player plays
    piece: specify which piece is played
    x: first coordinate
    y: second coordinate
    angle: orientation of the piece
    """
    c = get_db().cursor()
    c.executemany("INSERT INTO Moves VALUES ((?), (?), (?), (?)),", [gameid, movenumber, colour, piece, x, y, angle])
    get_db().commit()


def new_player(pid:str, password:str) -> bool:
    """
    Function to store a new user in the db if he doesn't already exist

    pid: player's id
    password: player's password

    Returns if the account was successfully created
    """
    if get_temp("*", "Players", "pid", pid):
        return False

    else:
        c = get_db().cursor()
        c.executemany("INSERT INTO Players VALUES ((?), (?), (?), (?)),", [pid, password, TODO, time()])
        get_db().commit()
        return True
    
def update_pid(pid:str, new_pid) -> bool:
    """
    Function to change the username

    pid: player's id
    new_pid: new player's id (new username)

    Returns if the change of username was successfull
    """
    if get_temp("*", "Players", "pid", new_pid):
        return False

    else:
        set_temp("Players", "pid", new_pid, "pid", pid)
        return True
    
def new_game(j1:str, j2:str, j3: str, j4: str):
    """
    Function to create a new game with the players's ids

    j1: first player's id (can be None)
    j2: second player's id (can be None)
    j3: thirs player's id (can be None)
    j4: fourth player's id (can be None)
    """
    c = get_db().cursor()

    gameid = TODO
    c.executemany("INSERT INTO Games VALUES ((?), (?), (?), (?)),", [gameid, j1, j2, j3, j4, False])
    get_db().commit()