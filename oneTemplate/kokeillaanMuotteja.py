from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
	fruits = ["apple", "pear", "peach"]
	return render_template("base.html", name="anna", fruits=fruits)

@app.route("/another")
def another():
	return render_template("another.html")

@app.route("/maths")
def maths():
	number = 1
	return render_template("maths.html", number=number)

app.run()

