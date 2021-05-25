from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
	fruits = ["apple", "pear", "peach"]
	return render_template("base.html", name= "AnNa",fruits=fruits)

@app.route("/another")
def another():
	return render_template("another.html")

app.run()

