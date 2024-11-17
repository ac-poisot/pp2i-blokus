# Database connection: getters and setters

import sqlite3
from app import get_db
from time import time

def get_temp(what:str, table:str, cond_a:str, cond_b:any) -> any:
    c = get_db().cursor()
    c.executemany("SELECT (?) FROM (?) WHERE (?) = (?);", [what, table, cond_a, cond_b])
    return c.fetchall()

def set_temp(table:str, what:str, towhat:any, cond_a:str, cond_b:any) -> None:
    c = get_db().cursor()
    c.execute("UPDATE (?) SET (?) = (?) WHERE (?) = (?);", [table, what, cond_a, cond_b])
    get_db().commit()


def get_password(pid:str) -> int:
    return get_temp("password", "Players", "pid", pid)

def get_token(pid:str) -> str:
    exp_date = get_temp("tokenexpiration", "Players", "pid", pid)
    if time() > exp_date:
        return None
    else:
        return get_temp("token", "Players", "pid", pid)

def get_game(gameid:int) -> list:
    return get_temp("*", "Games", "gameid", gameid)


def get_history(gameid:int) -> list:
    c = get_db().cursor()
    c.executemany("SELECT * FROM Moves WHERE gameid = (?) ORDER BY movenumber ASC;", [gameid])
    return c.fetchall()

def new_move(gameid:int, movenumber:int, colour:int, piece:int, x:int, y:int, angle:int) -> None:
    c = get_db().cursor()
    c.executemany("INSERT INTO Moves VALUES ((?), (?), (?), (?)),", [gameid, movenumber, colour, piece, x, y, angle])
    get_db().commit()


def new_player(pid:str, password:str) -> bool:
    if get_temp("*", "Players", "pid", pid):
        return False

    else:
        c = get_db().cursor()
        c.executemany("INSERT INTO Players VALUES ((?), (?), (?), (?)),", [pid, password, TODO, time()])
        get_db().commit()
        return True
    
def update_pid(pid:str, new_pid) -> bool:
    if get_temp("*", "Players", "pid", new_pid):
        return False

    else:
        set_temp("Players", "pid", new_pid, "pid", pid)
        return True
    
def new_game(j1:str, j2:str, j3: str, j4: str):
    c = get_db().cursor()

    gameid = TODO
    c.executemany("INSERT INTO Games VALUES ((?), (?), (?), (?)),", [gameid, j1, j2, j3, j4, False])
    get_db().commit()