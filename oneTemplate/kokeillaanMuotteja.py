from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
	fruits = ["apple", "pear", "peach"]
	return render_template("base.html", name= "Anna",fruits=fruits)

app.run()

