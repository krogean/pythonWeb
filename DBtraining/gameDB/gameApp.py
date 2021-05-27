from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy #m
from flask_wtf import FlaskForm #m
from wtforms.ext.sqlalchemy.orm import model_form #m

app = Flask(__name__)
app.secret_key = "OKqlatM5cHHil1penbae4aezie0zao" #m
db = SQLAlchemy(app) #m

class Game(db.Model): #m
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)

GameForm = model_form(Game, base_class=FlaskForm, db_session=db.session) #m!!!

@app.before_first_request #m
def initMe():
	db.create_all() #m
	
	game = Game(name="The great Game")
	db.session.add(game) #m

	game = Game(name="The boring Game")
	db.session.add(game)

	db.session.commit()

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/gamelist")
def gamelist():
	games = Game.query.all() #m
	return render_template("gamelist.html", games=games)

@app.route("/addgame", methods=["GET", "POST"])
def addgame():
	form = GameForm() #m

	if form.validate_on_submit(): #m
		game = Game() #m
		form.populate_obj(game) #m
		
		db.session.add(game) #m
		db.session.commit()

		print("New Game added")

	return render_template("addgame.html", form=form)


if __name__ == "__main__":
	app.run()
