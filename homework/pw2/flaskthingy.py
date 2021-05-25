from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def name():
	names = ["Anna", "Noora", "Jonna", "Laura"]
	return render_template("base.html", name="Anna", names=names)

@app.route("/first")
def first():
	return render_template("first.html")

@app.route("/second")
def second():
	return render_template("second.html")

app.run()
