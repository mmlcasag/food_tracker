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

@app.route('/day/<date_id>', methods=['GET'])
def get_day(date_id):
    db = open_db()
    cur = db.execute(' select d.id, d.entry_date from dates d where d.id = ? ', [date_id])
    date = cur.fetchone()

    date_db = datetime.strptime(str(date['entry_date']), '%Y%m%d')
    date_ft = datetime.strftime(date_db, '%B %d, %Y')
    
    cur = db.execute(' select f.id, f.name from foods f order by f.name ')
    foods = cur.fetchall()

    cur = db.execute(' select sum(f.protein) protein, sum(f.carbs) carbs, sum(f.fat) fat, sum(f.calories) calories from daily_intake i join dates d on d.id = i.date_id join foods f on f.id = i.food_id where i.date_id = ? ', [date_id])
    totals = cur.fetchone()

    cur = db.execute(' select i.date_id, d.entry_date, i.food_id, f.name, f.protein, f.carbs, f.fat, f.calories from daily_intake i join dates d on d.id = i.date_id join foods f on f.id = i.food_id where i.date_id = ? ', [date_id])
    intakes = cur.fetchall()

    return render_template('day.html', date_id=date_id, date_ft=date_ft, foods=foods, totals=totals, intakes=intakes)

@app.route('/day', methods=['POST'])
def post_day():
    date_id = request.form['date']
    food_id = request.form['food']

    values = [date_id, food_id]

    db = open_db()
    db.execute(' insert into daily_intake ( date_id, food_id ) values ( ?, ? ) ', values)
    db.commit()

    return redirect(url_for('get_day', date_id=date_id))

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
