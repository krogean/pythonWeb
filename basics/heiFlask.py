# used sources: terokarvinen.com and his course "Python Web Service From Idea to Production"
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hei():
	return "Hei Flaskin maailma!"

app.run()
