##############################################################################
# App Configuration:
##############################################################################

from flask import Flask, redirect, render_template, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
# app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ILuvHummingbirds321"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##############################################################################
# Root Route:
##############################################################################

@app.route("/", methods=["GET"])
def home():
    """Redirects to list of posts."""

    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("posts/home.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

##############################################################################
# User Routes:
##############################################################################

@app.route("/users", methods=["GET"])
def user_list():
    """List all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template("users/user_list.html", users=users)


@app.route("/users/add_user", methods=["GET"])
def show_add_user_form():
    """Show add_user form"""
    return render_template("users/add_user.html")


@app.route("/users/add_user", methods=["POST"])
def add_user():
    """Handle form submission for creating a new user"""
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash(f"User '{new_user.full_name}' added.")

    return redirect('/users')


@app.route("/users/user_details/<int:user_id>", methods=["GET"])
def show_user_details(user_id):
    """Show page with details about the user"""
    user = User.query.get_or_404(user_id)

    return render_template("users/user_details.html", user=user)


@app.route("/users/<int:user_id>/edit_user", methods=["GET"])
def show_edit_user_form(user_id):
    """Show the edit_user form."""
    user=User.query.get_or_404(user_id)

    return render_template("users/edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit_user", methods=["POST"])
def save_user_edits(user_id):
    """Handle form submission for editing an existng user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"],
    user.last_name = request.form["last_name"],
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    flash(f"User '{user.full_name}' edited.")

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/users")


########################################################################
# Post Routes:
########################################################################

@app.route("/users/<int:user_id>/posts/add_post", methods=["GET"])
def show_add_post_form(user_id):
    """Show add_post form."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/add_post.html', user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/add_post", methods=["POST"])
def add_post_to_db(user_id):
    """Handle form submission for adding a post for a user."""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title = request.form['title'],
        content = request.form['content'],
        user=user,
        tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/")

@app.route('/posts/<int:post_id>', methods=["GET"])
def show_posts(post_id):
    """Show a page with info for a specific post."""
    post = Post.query.get_or_404(post_id)

    return render_template('posts/post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit_post', methods=["GET"])
def show_edit_post_form(post_id):
    """Shows edit post form for editing an existing post."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('posts/edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit_post', methods=["POST"])
def save_post_edits(post_id):
    """Handle form submission for editing an existing post."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect (f"/users/user_details/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle form submission for deleting a post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/user_details/{post.user_id}")


######################################################################
# Tag Routes:
######################################################################

@app.route("/tags", methods=["GET"])
def tags_list():
    """List all tags"""
    tags = Tag.query.all()

    return render_template("tags/tag_list.html", tags=tags)


@app.route("/tags/tag_details/<int:tag_id>", methods=["GET"])
def show_tag_details(tag_id):
    """Show page with details about a tag."""
    tag = Tag.query.get_or_404(tag_id)

    return render_template("tags/tag_details.html", tag=tag)


@app.route("/tags/add_tag", methods=["GET"])
def show_add_tag_form():
    """Show add_tag form."""
    posts = Post.query.all()
    return render_template("tags/add_tag.html", posts=posts)


@app.route("/tags/add_tag", methods=["POST"])
def add_tag():
    """Handle form submission for creating a new tag."""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tags '{new_tag.name}' added.")

    return redirect('/tags')

@app.route("/tags/<int:tag_id>/edit_tag", methods=["GET"])
def show_edit_tag_form(tag_id):
    """Show the edit_tag form."""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template("tags/edit_tag.html", tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit_tag", methods=["POST"])
def save_tag_edits(tag_id):
    """Handle form submission for editing an existing tag."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Handle form submission for deleting an existing tag."""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")
