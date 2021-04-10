from flask import Flask, render_template, g, request, url_for, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

#

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

#

@app.route('/', methods=['GET'])
def get_home():
    db = open_db()
    cur = db.execute(' select id, entry_date from dates order by entry_date ')
    results = cur.fetchall()
    
    dates = []
    for i in results:
        db_date = datetime.strptime(str(i['entry_date']), '%Y%m%d')
        ft_date = datetime.strftime(db_date, '%B %d, %Y')

        single_date = {}
        single_date['id'] = i['id']
        single_date['entry_date'] = ft_date

        dates.append(single_date)

    return render_template('home.html', dates=dates)

@app.route('/', methods=['POST'])
def post_home():
    str_date = request.form['date']
    dat_date = datetime.strptime(str_date, '%Y-%m-%d')
    db_date = datetime.strftime(dat_date, '%Y%m%d')
    
    values = [ db_date ]

    db = open_db()
    db.execute(' insert into dates ( entry_date ) values ( ? )', values)
    db.commit()

    return redirect(url_for('get_home'))

@app.route('/day/<date>', methods=['GET'])
def get_day(date):
    db = open_db()
    cur = db.execute(' select id, entry_date from dates where entry_date = ? ', [date])
    result = cur.fetchone()

    db_date = datetime.strptime(str(result['entry_date']), '%Y%m%d')
    ft_date = datetime.strftime(db_date, '%B %d, %Y')

    cur = db.execute(' select id, name from foods order by name ')
    foods = cur.fetchall()

    return render_template('day.html', date=date, formatted_date=ft_date, foods=foods)

@app.route('/day', methods=['POST'])
def post_day():
    date = request.form['date']
    food = request.form['food']

    return ' Date: {} - Food: {}'.format(date, food)

@app.route('/add_food', methods=['GET'])
def get_add_food():
    db = open_db()
    cur = db.execute(' select id, name, protein, carbs, fat, calories from foods order by id ')
    foods = cur.fetchall()
    
    return render_template('add_food.html', foods=foods)

@app.route('/add_food', methods=['POST'])
def post_add_food():
    name = request.form['name']
    
    protein = int(request.form['protein'])
    carbs = int(request.form['carbs'])
    fat = int(request.form['fat'])
    
    calories = (protein * 4) + (carbs * 4) + (fat * 9)

    values = [name, protein, carbs, fat, calories]

    db = open_db()
    db.execute(' insert into foods ( name, protein, carbs, fat, calories ) values ( ?, ?, ?, ?, ? ) ', values)
    db.commit()

    return redirect(url_for('get_add_food'))
