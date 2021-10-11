from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug import datastructures
import bcrypt
import os


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

def autorize(func):
    def wrapper(*args, **kwargs):
        try:
            session['name'] != None
        except:
            flash("Prosím přihlašte se.", "error")
            return redirect(url_for('logn'))
        else:
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/')
def index():
    query = db.engine.execute('SELECT skola.nazev, mesto.nazev, obor.nazev, pocet_prijatych.pocet, pocet_prijatych.rok FROM mesto JOIN skola ON mesto.id=skola.mesto JOIN pocet_prijatych ON skola.id=pocet_prijatych.skola JOIN obor ON pocet_prijatych.obor=obor.id')
    return render_template("index.html", data=query)

@app.route('/map')
def map():
    queryMap = db.engine.execute('SELECT skola.nazev, mesto.nazev FROM mesto JOIN skola ON mesto.id=skola.mesto')
    return render_template("map.html", data=queryMap)

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        email = request.form['email']
        try:
            user = db.engine.execute(text("SELECT * FROM accounts WHERE username=:username"), username=username,).first()
            if user == None:
                db.engine.execute("INSERT INTO accounts (username, password, email) VALUES (%s, %s)"(username, hash_password, email))
                session['name'] = username
                flash("Registrace proběhla úspěšně", "success")
                return redirect(url_for("index"))
            else:
                flash("Uživatel s tímto jménem již existuje", "error")
                return redirect(url_for("register"))
        except Exception as e:
            print(e)
            return "chyba"
    

@app.route("/login", methods=["GET","POST"])
def login():
   if request.method == "POST":
      email = request.form['email']
      password = request.form['password'].encode( 'utf-8')

      user = db.engine.execute(text("SELECT * FROM accounts WHERE email=:email"),email=email,).first()

      if user != None:
         if bcrypt.hashpw(password, user[2].encode('utf-8')) == user[2].encode('utf-8'):
            session['name'] = user[1]
            return redirect(url_for("index"))
      flash("Jméno a heslo se neshodují", "error")
      return redirect(url_for("login"))
   else:
        return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)