##############################################################################
# App Configuration:
##############################################################################

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ILuvHummingbirds321"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##############################################################################
# App Routes:
##############################################################################

@app.route("/", methods=["GET"])
def home():
    """Redirects to users page"""
    return redirect("/user_list")


@app.route("/user_list", methods=["GET"])
def user_list():
    """Show user_list page"""
    user = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("user_list.html", user=user)


@app.route("/add_user", methods=["GET"])
def show_add_user_form():
    """Show add_user form"""
    return render_template("add_user.html")


@app.route("/add_user", methods=["POST"])
def add_user_to_db():
    """Handle form submission for creating a new user"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'], 
        image_url=request.form['image_url'] or None)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/user_list')


@app.route("/user_details/<int:user_id>")
def show_user_details(user_id):
    """Show page with details about the user"""
    user=User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.route("/user_details/<int:user_id>/edit")
def show_edit_user_form(user_id):
    """Show the edit_user form."""
    user=User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/user_details/<int:user_id>/edit", methods=["POST"])
def save_user_edits(user_id):
    """Handle form submission for editing an existng user"""
    user=User.query.get_or_404(user_id)
    user.first_name=request.form["first_name"],
    user.last_name=request.form["last_name"], 
    user.image_url=request.form["image_url"] or None
    db.session.add(user)
    db.session.commit()
    return redirect("/user_list")


@app.route("/user_details/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/user_list")



