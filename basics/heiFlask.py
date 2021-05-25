from flask import Flask
app = Flask(__name__)

@app.route("/")
def hei():
	return "Hei Flaskin maailma!"

app.run()
