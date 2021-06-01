# used sources: terokarvinen.com and his course "Python Web Service From Idea to Production"
from flask import Flask, render_template

#app on uusi muuttuja, Flask on olio
app = Flask(__name__) 
#jos oltaisiin importoitu ihan vaan flask, niin tässä lukisi flask.Flask

@app.route("/")
def index():
	return render_template("base.html")

app.run() #saa käyttää vain(!) testiympäristössä
