from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "super secret key"
app.config.from_object('config')

db = SQLAlchemy(app)

#decorator for unauthorized access
def authorize(func):
   def wrapper(*args, **kwargs):
      try:
         session['name'] != None
      except:
         flash("Vaše relace vypršela. Prosím přihlašte se.", "error")
         return redirect(url_for('login'))
      else:
        return func(*args, **kwargs)
   wrapper.__name__ = func.__name__
   return wrapper

@app.route("/")
def index():
   fields = db.engine.execute('SELECT * FROM obor')
   cities = db.engine.execute('SELECT * FROM mesto')
   years = db.engine.execute('SELECT DISTINCT rok FROM pocet_prijatych')
   query = db.engine.execute('SELECT skola.nazev, mesto.nazev, obor.nazev, pocet_prijatych.pocet, pocet_prijatych.rok FROM mesto JOIN skola ON mesto.id=skola.mesto JOIN pocet_prijatych ON skola.id=pocet_prijatych.skola JOIN obor ON pocet_prijatych.obor=obor.id')
   result = []
   for row in query:
      result.append(row)
   return render_template("index.html", data=result, cities=cities, fields=fields, years=years)

@app.route('/addSchool', methods=["GET","POST"])
@authorize
def addSchool():
   if request.method == 'GET':
      fields = db.engine.execute('SELECT * FROM obor')
      cities = db.engine.execute('SELECT * FROM mesto')
      return render_template('add_school.html', fields=fields, cities=cities)
   else:
      school = request.form['school']
      geoLat = request.form['geoLat']
      geoLong = request.form['geoLong']
      city = request.form['city']
      field = request.form['field']
      num_of_accepted = request.form['num_of_accepted']
      year = request.form['year']
      try:
         db.engine.execute("INSERT INTO skola (nazev, mesto, geo_lat, geo_long) VALUES ('%s', %s, %s, %s)" % (school, city, geoLat, geoLong))
         insertedSchoolId = db.engine.execute("SELECT id FROM skola WHERE nazev='%s'" % (school)).first()
         db.engine.execute("INSERT INTO pocet_prijatych (obor, skola, pocet, rok) VALUES ('%s', %s, %s, %s)" % (field, insertedSchoolId[0], num_of_accepted, year))

         flash("Ukládání proběhlo úspěšně.", "success")
         return redirect(url_for("index"))
      except Exception as e:
         print(e)
         flash("Při ukládání se vyskytla chyba.", "error")
         return redirect(url_for("index"))
      
@app.route('/addCity', methods=["GET","POST"])
@authorize
def addCity():
   if request.method == 'GET':
      return render_template('new_city.html')
   else:
      name = request.form['name']
      try:
         db.engine.execute("INSERT INTO mesto (nazev) VALUES ('%s')" % (name))
         flash("Ukládání proběhlo úspěšně.", "success")
      except Exception as e:
         flash("Při ukládání se vyskytl problém." + str(e), "error")
      return redirect(url_for("index"))
      

@app.route('/addField', methods=["GET","POST"])
@authorize
def addField():
   if request.method == 'GET':
      return render_template('new_field.html')
   else:
      name = request.form['name']
      try:
         db.engine.execute("INSERT INTO obor (nazev) VALUES ('%s')" % (name))
         flash("Ukládání proběhlo úspěšně.", "success")
      except:
         flash("Při ukládání se vyskytl problém.", "error")
      return redirect(url_for("index"))
      

@app.route('/map')
@authorize
def map():
    queryMap = db.engine.execute('SELECT skola.nazev, mesto.nazev FROM mesto JOIN skola ON mesto.id=skola.mesto')
    return render_template("map.html", data=queryMap)

@app.route('/register', methods=["GET","POST"])
def register():
   if request.method == 'GET':
      return render_template('register.html')
   else:
      username = request.form['username']
      password = request.form['password'].encode('utf-8')
      hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
      email = request.form['email']
      try:
         user = db.engine.execute(text("SELECT * FROM accounts WHERE username=:username"),username=username,).first()
         if user == None:
            db.engine.execute("INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)",(username,hash_password, email))
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
      username = request.form['username']
      password = request.form['password'].encode('utf-8')

      user = db.engine.execute(text("SELECT * FROM accounts WHERE username=:username"),username=username,).first()

      if user != None:
         if bcrypt.hashpw(password, user[2].encode('utf-8')) == user[2].encode('utf-8'):
            session['name'] = user[1]
            return redirect(url_for("index"))
      flash("Jméno a heslo se neshodují", "error")
      return redirect(url_for("login"))
   else:
        return render_template('login.html')

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for("login"))

if __name__ == "__main__":
   app.run(debug=True)