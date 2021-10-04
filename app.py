from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug import datastructures


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

@app.route('/')
def index():
    query = db.engine.execute('SELECT skola.nazev, mesto.nazev, obor.nazev, pocet_prijatych.pocet, pocet_prijatych.rok FROM mesto JOIN skola ON mesto.id=skola.mesto JOIN pocet_prijatych ON skola.id=pocet_prijatych.skola JOIN obor ON pocet_prijatych.obor=obor.id')
    return render_template("index.html", data=query)

@app.route('/map')
def map():
    queryMap = db.engine.execute('SELECT skola.nazev, mesto.nazev FROM mesto JOIN skola ON mesto.id=skola.mesto')
    return render_template("map.html", data=queryMap)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)