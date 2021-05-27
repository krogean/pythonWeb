from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "CohlahT9chiel0onibae4eesee9zee"
db = SQLAlchemy(app)

# Create Contact Class
class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	phonenumber = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	#for testing purpouses only name for now

ContactForm = model_form(Contact, base_class=FlaskForm, db_session=db.session)

# Init DB and give example data
@app.before_first_request
def initDB():
	db.create_all()

	contact = Contact(name="Maija Mehiläinen", phonenumber="+358 445566778", email="maija.mehi@email.com")
	db.session.add(contact)
	contact = Contact(name="Esko Esimerkki", phonenumber="+358 556677889", email="esko.esim@email.com")
	db.session.add(contact)
	contact = Contact(name="Joe Jones", phonenumber="+358 982064982", email="joe@imthebest.com")
	db.session.add(contact)
	
	db.session.commit()
# List of contacts
@app.route("/")
def index():
	contacts = Contact.query.all()
	return render_template("index.html", contacts=contacts)

# Add new contact
@app.route("/new", methods=["GET", "POST"])
def addContact():
	contact = Contact()
	
	form = ContactForm()
	if form.validate_on_submit():
		form.populate_obj(contact)
		db.session.add(contact)
		db.session.commit()

		print("Contact added")
		return redirect("/")
	
	return render_template("addcontact.html", form=form)

# Edit contact
@app.route("/<int:id>/edit", methods=["GET","POST"])
def editContact(id):
	contact = Contact.query.get_or_404(id)
	form = ContactForm(obj=contact)

	if form.validate_on_submit():
		form.populate_obj(contact)
		db.session.add(contact)
		db.session.commit()

		print("Contact edited")
		return redirect("/")
	return render_template("addcontact.html", form=form)

@app.route("/<int:id>/delete")
def deleteContact(id):
	contact = Contact.query.get_or_404(id)
	db.session.delete(contact)
	db.session.commit()
	
	print("Contact deleted")
	return redirect("/")
		
if __name__ == "__main__":
	app.run()
