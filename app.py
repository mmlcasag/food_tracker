from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/day')
def day():
    return render_template('day.html')

@app.route('/add_food')
def add_food():
    return render_template('add_food.html')

