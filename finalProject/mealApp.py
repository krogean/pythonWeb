from flask import Flask, render_template, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash

#from views import * 

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = "asl2dhkadfwsguo2jalfkh76nalk7jlak5fn"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///anna'

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, nullable=False, unique=True)
	passwordHash = db.Column(db.String, nullable=False)
	
	def setPassword(self, password):
		self.passwordHash = generate_password_hash(password)

	def checkPassword(self, password):
		return check_password_hash(self.passwordHash, password)

	def __str__(self):
		return f"<User { escape(self.email) }>"

class Meal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	kcal = db.Column(db.Integer, nullable=True)
	userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	user = db.relationship("User", backref=db.backref("Meals", lazy=True))
	#time = db.Column()

MealForm = model_form(Meal, base_class=FlaskForm, db_session=db.session, exclude="user")

@app.before_first_request
def initDB():
	db.create_all()


#	user = User(email="maija@mehilainen.com")
#	user.setPassword("amppari")
#	db.session.add(user)

#	meal = Meal(name="Veggie Pizza", kcal=500, userId=user)
#	db.session.add(meal)
	
#	meal = Meal(name="Broccoli with egg", userId=user)
#	db.session.add(meal)


	db.session.commit()

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/list")
def mealList():
	meals = Meal.query.all()
	return render_template("mealList.html", meals=meals)

@app.route("/new", methods=["GET", "POST"])
def newMeal():
	loginRequired()
	meal = Meal()
	form = MealForm()
	if form.validate_on_submit():
		form.populate_obj(meal)
		meal.user = User.query.get(session["uid"])
		db.session.add(meal)
		db.session.commit()

		flash("Meal added!")
		return redirect("/list")
	return render_template("new.html", form=form)

@app.route("/<int:id>/edit", methods=["GET", "POST"])
def editMeal(id):
	loginRequired()
	meal = Meal.query.get_or_404(id)
	form = MealForm(obj=meal)
	if form.validate_on_submit():
		form.populate_obj(meal)
		db.session.add(meal)
		db.session.commit()

		flash("Meal edited!")
		return redirect("/list")
	return render_template("new.html", form=form)

@app.route("/<int:id>/delete")
def deleteMeal(id):
	loginRequired()
	meal = Meal.query.get_or_404(id)
	db.session.delete(meal)
	db.session.commit()

	flash("Meal deleted!")
	return redirect("/list")

#Errors
@app.errorhandler(404)
def custom404(e):
	return render_template("404.html")

@app.errorhandler(403)
def custom403(e):
	return redirect("/login")



# #User things ###TÄSTÄ EI MISTÄÄN MUISTANU MITÄÄN###!!!!!!!!!
class UserForm(FlaskForm):
	email = StringField("email", validators=[validators.Email()])
	password = PasswordField("password", validators=[validators.InputRequired()])

class RegisterForm(UserForm):
	key = StringField("registration key", validators=[validators.InputRequired()])


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
		return redirect("/list")
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



