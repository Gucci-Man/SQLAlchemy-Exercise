"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
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

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_code = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user_posts = db.relationship("User", backref="posts")

    tags = db.relationship("Tag", secondary="post_tags", backref="posts")

    post_tags = db.relationship("PostTag", backref="post_tags")


# Tag Model
class Tag(db.Model):
    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)


# PostTag Model
# Drop this table first when dropping and creating new tables
class PostTag(db.Model):
    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id"), primary_key=True)
