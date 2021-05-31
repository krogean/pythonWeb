from flask import Flask, render_template, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy #m
from flask_wtf import FlaskForm # m
from wtforms.ext.sqlalchemy.orm import model_form # m
from wtforms import StringField, PasswordField, validators #m
from werkzeug.security import generate_password_hash, check_password_hash #m!!!

app = Flask(__name__)
db = SQLAlchemy(app) #m
app.secret_key = "asldhkadfjalfkhnalkejlakfn"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///anna'

# Creating Book-class
class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	desc = db.Column(db.String, nullable=False)

BookForm = model_form(Book, base_class=FlaskForm, db_session=db.session) #m

@app.before_first_request
def initDB():
	db.create_all()

	book = Book(name="Twilight", desc="Sparkly dudes and dudettes")
	db.session.add(book)
	
	book = Book(name="Harry Potter", desc="Dude with a scar does magic or smt")
	db.session.add(book)

	user = User(email="maija@mehilainen.com")
	user.setPassword("amppari")
	db.session.add(user)

	db.session.commit()

#CRUD views

@app.route("/")
def index():
	books = Book.query.all()
	return render_template("index.html", books=books)

@app.route("/addDesc", methods=["GET", "POST"])
def addDesc():
	loginRequired()
	book = Book()
	form = BookForm()
	if form.validate_on_submit():
		form.populate_obj(book)
		db.session.add(book)
		db.session.commit()

		print("Book added")
		flash("Book description added!")
		return redirect("/")
	return render_template("addDesc.html", form=form)

@app.route("/<int:id>/edit", methods=["GET", "POST"])
def editDesc(id):
	loginRequired()
	book = Book.query.get_or_404(id)  #m
	form = BookForm(obj=book)  #m
	if form.validate_on_submit():
		form.populate_obj(book)
		db.session.add(book)
		db.session.commit()

		print("Book edited")
		flash("Book description edited!")
		return redirect("/")
	return render_template("addDesc.html", form=form)

@app.route("/<int:id>/delete")
def deleteDesc(id):
	loginRequired()
	book = Book.query.get_or_404(id) #m
	db.session.delete(book)
	db.session.commit()
	
	print("Book deleted")
	flash("Book deleted!")
	return redirect("/")

#Errors
@app.errorhandler(404)
def custom404(e):
	return render_template("404.html")

@app.errorhandler(403)
def custom403(e):
	return redirect("/login")



#User things ###TÄSTÄ EI MISTÄÄN MUISTANU MITÄÄN###!!!!!!!!!
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, nullable=False, unique=True)
	passwordHash = db.Column(db.String, nullable=False)
	
	def setPassword(self, password):
		self.passwordHash = generate_password_hash(password)

	def checkPassword(self, password):
		return check_password_hash(self.passwordHash, password)

class UserForm(FlaskForm):
        email = StringField("email", validators=[validators.Email()])
        password = PasswordField("password", validators=[validators.InputRequired()])

class RegisterForm(UserForm):
        key = StringField("registration key",
		validators=[validators.InputRequired()])

def currentUser():
        try:
                uid = int(session["uid"])
        except:
                return None
        return User.query.get(uid)

app.jinja_env.globals["currentUser"] = currentUser 

def loginRequired(): 
	if not currentUser(): 
		abort(403) 

@app.route("/login", methods=["GET", "POST"])
def loginView():
	form = UserForm()
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
		user = User.query.filter_by(email=email).first()
		if not user:
			flash("Bad username or password.")
			print("No such user")
			return redirect("/login")
		if not user.checkPassword(password):
			flash("Bad username or password.")
			print("Bad password")
			return redirect("/login")
		flash("Logged in. Welcome!")
		session["uid"]=user.id
		return redirect("/")
	return render_template("login.html", form=form)

@app.route("/logout")
def logoutView():
        session["uid"]=None
        flash("Logged out. Bye bye!")
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def registerView():
        form = RegisterForm()
        if form.validate_on_submit():
                if form.key.data != "anna":
                        flash("Bad registration key.")
                        return redirect("/register")
                user = User()
				if User.query.filter_by(email=user.email).first():
					flash("User already exits. Please log in!")
					return redirect("/login")
                user.email = form.email.data
                user.setPassword(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash("User created. Now, log in!")
                return redirect("/login")
        return render_template("register.html", form=form)



if __name__ == "__main__":
	app.run()




	
