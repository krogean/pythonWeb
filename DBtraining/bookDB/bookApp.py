# Used sources: terokarvinen.com and his course "Python Web Service From Idea to Production"

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy #m
from flask_wtf import FlaskForm #m!!!
from wtforms.ext.sqlalchemy.orm import model_form #m!!!

app = Flask(__name__)
db = SQLAlchemy(app) #m
app.secret_key = "OKqlatM5cHHil1penbae4aezie0zao" #m

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)

BookForm = model_form(Book, base_class=FlaskForm, db_session=db.session) #m!!!!

@app.before_first_request #m
def initMe():
	db.create_all() #m	

	book = Book(name="Maailman paras kirja")
	db.session.add(book)

	book = Book(name="Alamaailman huonoin kirja")
	db.session.add(book)
	
	db.session.commit()
	
@app.route("/")
def index():
	books = Book.query.all()
	return render_template("base.html", books=books)

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/new", methods=["GET", "POST"])
def newBook():
	book = Book() #m
	if id:
		book = Book.query.get_or_404(id)	
	
	form = BookForm(obj=book) #m

	if form.validate_on_submit(): #m
		form.populate_obj(book) #m
		db.session.add(book) #m
		db.session.commit() #m
		
		print("New book added!")	
	
	return render_template("new.html", form=form)

if __name__ == "__main__":
	app.run()
