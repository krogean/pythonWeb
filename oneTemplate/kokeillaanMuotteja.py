from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
	fruits = ["apple", "pear", "peach"]
	return render_template("base.html", name="anna", fruits=fruits)

@app.route("/another", methods=["GET", "POST"])
def another():
	return render_template("another.html")

@app.route("/maths")
def maths():
	return render_template("maths.html")

@app.route("/prkl")
def prkl():
	return render_template("prkl.html")

app.run()

