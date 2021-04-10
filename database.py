from flask import g
import sqlite3

def connect_db():
    sql = sqlite3.connect('/home/mmlcasag/python/food_tracker/database/food_tracker.db')
    sql.row_factory = sqlite3.Row
    return sql

def open_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db

def close_db():
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()
