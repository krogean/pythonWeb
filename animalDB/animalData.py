from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "cie1Eehop9IeX6Eisoh0aeseweengo"
db = SQLAlchemy(app)

class Animal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	species = db.Column(db.String, nullable=False)
	name = db.Column(db.String, nullable=True)
	age = db.Column(db.Integer, nullable=False)

AnimalForm = model_form(Animal, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initMe():
	db.create_all()

	animal = Animal(species="hamster", name="Hamtaro", age="1")
	db.session.add(animal)
	
	animal = Animal(species="human", name="Dude", age="90")
	db.session.add(animal)

	animal = Animal(species="lion", name="Simba", age="11")
	db.session.add(animal)

	db.session.commit()
	

@app.route("/", methods=["GET", "POST"])
def index():
	animals = Animal.query.all()

	animalForm = AnimalForm()
	print(request.form)	
	
	return render_template("animalList.html", animals=animals, form=animalForm)

if __name__ == "__main__":
	app.run()
