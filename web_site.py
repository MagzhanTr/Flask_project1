from flask import Flask, redirect, url_for, render_template, request, session, flash
import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

VIDEO_FOLDER = os.path.join('static')

app = Flask(__name__)
app.secret_key = "Nautilus"
app.permanent_session_lifetime = timedelta(days=5)
app.config['UPLOAD_FOLDER'] = VIDEO_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

db = SQLAlchemy(app)

class users(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))

	def __init__(self, name):
		self.name = name

@app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
	return render_template("view.html", values=users.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
	video_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'bg_login.mp4')
	if request.method == "POST":
		session.permanent = True
		user_name = request.form["user_name"]
		user_password = request.form["user_password"]
		session["user_name"] = user_name
		session["user_password"] = user_password
		
		usr = users(user_name)
		db.session.add(usr)
		db.session.commit()

		return redirect(url_for("user_page"))
	if "user_name" in session:
		return redirect(url_for("user_page"))
	return render_template("login.html", video = video_filename)

@app.route("/user")
def user_page():
	if "user_name" in session:
		user_name = session["user_name"]
		return render_template("user.html", user=user_name)
	return redirect(url_for("login"))

@app.route("/logout")
def logout():
	if "user_name" in session:
		user_name = session["user_name"]
		flash(f"Logout has been successfully, {user_name}!", "info")
	session.pop("user_name", None)
	session.pop("user_password", None)
	return redirect(url_for("login"))

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)