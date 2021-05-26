from flask import Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "ipqkviaeu97ybp0o287lvam5xuyks"
db = SQLAlchemy(app)

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	genre = db.Column(db.String, nullable=False)
	price = db.Column(db.Float)

GameForm = model_form(Game, base_class=FlaskForm,db_session=db.session)

@app.before_first_request
def initMe():
	db.create_all()
	game = Game(name="WoW", genre="MMORPG")
	db.session.add(game)
	game = Game(name="Ark Survival Evolved", genre="Survival MMO")
	db.session.add(game)
	game = Game(name="Resident Evil", genre="Action Horror")
	db.session.add(game)

	db.session.commit()

@app.route("/")
def base():
	return render_template("base.html")

@app.route("/one")
def first():
	return render_template("one.html")

@app.route("/gamelist")
def gamelist():
	games = Game.query.all()
	return render_template("gamelist.html", games=games)

@app.route("/addgame", methods=["GET", "POST"])
def addgame():
	gameForm = GameForm()
	print(request.form)
	return render_template("addgame.html", form=gameForm)

@app.route("/msg")
def msgPage():
	flash("This is a secret message just for you.")
	return redirect("/")

@app.route("/onemsg")
def oneMsgPage():
	flash("This is another secret message just for you.")
	return redirect("/one")

if __name__ == "__main__":
	app.run()
