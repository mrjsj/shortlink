from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import func
from .extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    created_date = db.Column(db.DateTime(), server_default=func.now())

    links_created = db.relationship(
        "Link",
        foreign_keys="Link.user_id",
        backref="creator",
        lazy=True
    )

    @property
    def unhashed_password(self):
        raise AttributeError("Cannot view unhashed password!")

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(2048))
    shortlink = db.Column(db.String(8))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_date = db.Column(db.DateTime(), server_default=func.now())
