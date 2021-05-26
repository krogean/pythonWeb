from flask import Flask

#app on uusi muuttuja, Flask on olio
app = Flask(__name__) 
#jos oltaisiin importoitu ihan vaan flask, niin tässä lukisi flask.Flask

@app.route("/")
def index():
	return "Jee toimii"

app.run() #saa käyttää vain(!) testiympäristössä
