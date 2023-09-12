"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
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

# drop existing tables and create new ones
""" db.drop_all()
db.create_all() """


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

    if len(image_url) == 0:
        image_url = None  # if image_url is empty, then make it NULL

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show information about the given user."""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Show the edit page for a user."""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def post_edit(user_id):
    """Process the edit form"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    if len(image_url) != 0:
        User.query.filter_by(user_id=user_id).update({"image_url": f"{image_url}"})
        db.session.commit()

    if len(first_name) != 0:
        User.query.filter_by(user_id=user_id).update({"first_name": f"{first_name}"})
        db.session.commit()

    if len(last_name) != 0:
        User.query.filter_by(user_id=user_id).update({"last_name": f"{last_name}"})
        db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete(user_id):
    """Delete the user"""
    User.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return redirect("/users")
