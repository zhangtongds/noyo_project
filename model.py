from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Person(db.Model):
    """The person model."""

    __tablename__ = "person"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(25), nullable=True)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    age = db.Column(db.String(15))

    def __init__(self, user_id, first_name, middle_name, last_name, email, age):
        self.user_id = user_id
        self.first_name = first_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.age = age

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id={} first_name={} middle_name={} last_name={} email={} age={} >".format(self.user_id, self.first_name, self.middle_name, self.last_name, self.email, self.age)


def connect_to_db(app):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///person"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to person DB.")
