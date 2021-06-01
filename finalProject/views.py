from flask import Flask, render_template, redirect, flash, session, abort
#from flask_sqlalchemy import SQLAlchemy
#from flask_wtf import FlaskForm
#from wtforms.ext.sqlalchemy.orm import model_form
#from wtforms import StringField, PasswordField, validators
#from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
#db = SQLAlchemy(app)
#app.secret_key = "asl2dhkadfwsguo2jalfkh76nalk7jlak5fn"
#app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///anna'


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
		return redirect("/")
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



