from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String, nullable=False)

@app.before_first_request
def initMe():
	db.create_all()

	todo = Todo(content="Pese pyykkiä")
	db.session.add(todo)

	todo = Todo(content="Vie roskat")
	db.session.add(todo)

	db.session.commit()

@app.route("/")
def index():
	todos = Todo.query.all()
	return render_template("index.html", todos=todos)	

if __name__ == "__main__":
	app.run()
