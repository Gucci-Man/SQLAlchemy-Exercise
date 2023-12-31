"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import *


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
    tags = db.session.query(Tag).all()
    return render_template("list.html", users=users, tags=tags)


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
    posts = Post.query.filter(Post.user_code == user_id)
    return render_template("details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Show the edit page for a user."""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def post_edit(user_id):
    """Process the user edit form"""
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
    posts = Post.query.filter_by(user_code=user_id).all()

    # if user have posts, delete those post tags then posts
    if len(posts) != 0:
        for post in posts:
            post_tags = PostTag.query.filter_by(post_id=post.post_id).all()
            # Delete all connected Post Tags first
            if len(post_tags) != 0:
                for pt in post_tags:
                    PostTag.query.filter_by(post_id=post.post_id).delete()
                    db.session.commit()

            Post.query.filter_by(post_id=post.post_id).delete()
            db.session.commit()

    User.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    tags = db.session.query(Tag).all()  # Get list of tags to add for post

    return render_template("new_post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def handle_new_post(user_id):
    """Handle add post form, add post and redirect to the user detail page"""
    # First handle adding post
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title, content=content, user_code=user_id)
    db.session.add(new_post)
    db.session.commit()

    # Next handle creating the Post Tags
    tags = request.form.getlist("tags_list")  # returns a list of selected tag_ids
    if len(tags) != 0:
        for tag in tags:
            pt = PostTag(post_id=new_post.post_id, tag_id=tag)
            db.session.add(pt)
            db.session.commit()

    return redirect(f"/users/{user_id}")


# TODO - show tags for that post
@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    """Show a post. Show buttons to edit and delete the post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_code)
    tags = post.tags

    return render_template("post_detail.html", post=post, user=user, tags=tags)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_code)
    tags = db.session.query(Tag).all()  # Get list of tags to add for post editing

    # Delete the Post tags to make room for new ones
    post_tags = PostTag.query.filter_by(post_id=post_id).all()

    # Deleting all connected Post Tags
    if len(post_tags) != 0:
        for pt in post_tags:
            PostTag.query.filter_by(post_id=post_id).delete()
            db.session.commit()

    return render_template("edit_post.html", post=post, user=user, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view"""
    # First handle editing posts
    title = request.form["title"]
    content = request.form["content"]
    Post.query.filter_by(post_id=post_id).update({"title": f"{title}"})
    Post.query.filter_by(post_id=post_id).update({"content": f"{content}"})
    db.session.commit()

    # Next handle updating the Post Tags
    tags = request.form.getlist("tags_list")
    if len(tags) != 0:
        for tag in tags:
            pt = PostTag(post_id=post_id, tag_id=tag)
            db.session.add(pt)
            db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a post"""
    post_tags = PostTag.query.filter_by(post_id=post_id).all()

    # Delete all connected Post Tags first
    if len(post_tags) != 0:
        for pt in post_tags:
            PostTag.query.filter_by(post_id=post_id).delete()
            db.session.commit()

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_code)
    Post.query.filter_by(post_id=post_id).delete()
    db.session.commit()

    return redirect(f"/users/{user.user_id}")


@app.route("/tags")
def tags():
    """List all tags, with links to the tag detail page"""
    tags = db.session.query(Tag).all()

    return render_template("tag_list.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """Show details about a tag. Have links to edit form and to delete"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag_detail.html", tag=tag, posts=posts)


@app.route("/tags/new")
def new_tag():
    """Shows a form to add a new tag"""
    return render_template("add_tag.html")


@app.route("/tags/new", methods=["POST"])
def new_tag_post():
    """Process add form, adds tag, and redirect to tag list."""
    tag_name = request.form["tag_name"]
    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """Show edit form for a tag."""
    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag_post(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""
    tag_name = request.form["tag_name"]

    Tag.query.filter_by(tag_id=tag_id).update({"name": f"{tag_name}"})
    db.session.commit()

    return redirect(f"/tags/{tag_id}")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag."""
    post_tags = PostTag.query.filter_by(tag_id=tag_id).all()

    # Delete all connected Post Tags first
    if len(post_tags) != 0:
        for pt in post_tags:
            PostTag.query.filter_by(tag_id=tag_id).delete()
            db.session.commit()

    Tag.query.filter_by(tag_id=tag_id).delete()
    db.session.commit()

    return redirect("/tags")
