"""Models for Blogly"""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# MODELS FOR BLOGLY:

class User(db.Model): 
    """User model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Blog post model."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def formatted_datetime(self):
        """Return formatted date/time.""" 
        return self.created_at.strftime("%B/%-d/%Y %-I/%M/%p")


class PostTag(db.Model): 
    """Tags Posts."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)


class Tag(db.Model):
    """Tag to add to posts."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post', 
        secondary="posts_tags",
        backref="tags",
    )


def connect_db(app):
    """Connect the database to app.py"""
    db.app = app
    db.init_app(app)
