"""Models for Blogly"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""Models for Blogly."""

class User(db.Model): 
    """User model."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.Text,
                        nullable=True,
                        unique=False)
    last_name = db.Column(db.Text,
                       nullable=False,
                       unique=False)
    image_url = db.Column(db.Text,
                       nullable=True,
                       unique=True)


def connect_db(app):
    """Connect the database to app.py"""
    db.app = app
    db.init_app(app)



