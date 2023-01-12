import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/mreview", methods=["GET", "POST"])
def make_review():

    if request.method == 'POST':

        state = request.form.get('state').upper()
        name = request.form.get('name')
        p_comment = request.form.get('p_comment')

        if not state:
            return render_template('error.html')

        if not name:
            return render_template('error.html')

        try:
            pollution = int(request.form.get("pollution"))
            restaurants = int(request.form.get('restaurants'))
            crowd = int(request.form.get('crowd'))
            water = int(request.form.get('water'))
            waves = int(request.form.get('waves'))
            accessability = int(request.form.get('accessability'))
            facilities = int(request.form.get('facilities'))
        except:
            return render_template('error.html')

        if pollution <= 0 or pollution >= 11:
            return render_template('error.html')
        if restaurants <= 0 or restaurants >= 11:
            return render_template('error.html')
        if crowd <= 0 or crowd >= 11:
            return render_template('error.html')
        if water <= 0 or water >= 11:
            return render_template('error.html')
        if waves <= 0 or waves >= 11:
            return render_template('error.html')
        if accessability <= 0 or accessability >= 11:
            return render_template('error.html')
        if facilities <= 0 or facilities >= 11:
            return render_template('error.html')
        if not p_comment:
            return render_template('error.html')

        db.execute('INSERT INTO reviews (state, name, pollution, restaurants, crowd, water, waves, accessability, facilities, p_comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        state, name, pollution, restaurants, crowd, water, waves, accessability, facilities, p_comment)

        return redirect('/')

    else:
        return render_template('mreview.html')

@app.route("/sreviews")
def see_reviews():

    reviews = db.execute('SELECT state, name, pollution, restaurants, crowd, water, waves, accessability, facilities, p_comment, time FROM reviews ORDER BY time DESC')

    return render_template('sreviews.html', reviews=reviews)