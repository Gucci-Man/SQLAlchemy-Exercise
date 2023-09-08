"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from sqlalchemy import text


app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "IAMBATMAN"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home():
    """Redirects to list of users"""
    return redirect("/users")


@app.route("/users")
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template("list.html", users=users)


@app.route("/users/new")
def new_user():
    """Show an add form for users"""
    return render_template("form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """process the add form, adding a new user and going back to /users"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about a user"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)
