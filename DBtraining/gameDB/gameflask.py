from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("base.html")

@app.route("/list")
def listGames():
	return render_template("list.html")

app.run()
