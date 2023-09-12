"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, DateTime, func
import datetime

# initialize SQLAlchemy
db = SQLAlchemy()


# connect app with SQLAlchemy
def connect_db(app):
    db.app = app
    db.init_app(app)


# User Model
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False, unique=True)

    image_url = db.Column(
        db.String(500),
        nullable=True,
        default="https://img.freepik.com/premium-vector/people-icon-person-symbol-vector-illustration_276184-166.jpg?w=2000",
    )


# Post Model
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    user_code = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    assignments = db.relationship("User", backref="posts")
