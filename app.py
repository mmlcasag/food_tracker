from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('/home/mmlcasag/python/food_tracker/database/food_tracker.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/day')
def day():
    return render_template('day.html')

@app.route('/add_food')
def add_food():
    return render_template('add_food.html')
