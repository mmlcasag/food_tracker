from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('/home/mmlcasag/python/food_tracker/database/food_tracker.db')
    sql.row_factory = sqlite3.Row
    return sql

def open_db():
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

@app.route('/add_food', methods=['GET'])
def get_add_food():
    return render_template('add_food.html')

@app.route('/add_food', methods=['POST'])
def post_add_food():
    food_name = request.form['food-name']
    
    protein = int(request.form['protein'])
    carbs = int(request.form['carbs'])
    fat = int(request.form['fat'])
    
    calories = (protein * 4) + (carbs * 4) + (fat * 9)

    values = [food_name, protein, carbs, fat, calories]

    db = open_db()
    db.execute(' insert into foods ( name, protein, carbs, fat, calories ) values ( ?, ?, ?, ?, ? ) ', values)
    db.commit()

    return render_template('add_food.html')
