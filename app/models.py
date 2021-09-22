"""
Author: Courtney Amm
File: models.py

This file contains all of the database model classes used by SQLAlchemy to store rows from
the database as objects.

"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

# Database Models ####################################################################


class Food(db.Model):
    """
    A database table representing each food item, including it's name, model path, and nutritional
    info
    """
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(64), index=True, unique=True)
    model_path = db.Column(db.String(120), index=True, unique=True)
    collision_radius = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Float, nullable=False)
    fiber = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    saturated_fat = db.Column(db.Float, nullable=False)
    trans_fat = db.Column(db.Float, nullable=False)
    monounsaturated_fat = db.Column(db.Float, nullable=False)
    polyunsaturated_fat = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    in_portions = db.relationship('FoodsInPortions', backref='food', lazy=True)

    def __repr__(self):
        """
        This function tells python how to "print" the class, which is helpful for debugging.
        In this case, it returns the foods name and model path.
        """
        return "<food {}>".format(self.food_name) + "<model_path {}".format(self.model_path)


class User(db.Model, UserMixin):
    """
    Database that stores users
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(64), index=True, nullable=False)
    portions = db.relationship('Portion', backref='user', lazy=False)

    def set_password(self, password):
        """
        Takes the user's inputed password and creates a password hash to be stored on the server
        :param password: the password to be set as the user's password
        :return: void
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        checks the inputted password's hash against the user's saved password hash
        :param password: the password to be checked against the saved hash
        :return: boolean: if the password hashes match or not
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Portion(db.Model):
    """
    Database that stores each user's created potions
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.String(128), index=True, nullable=False)
    notes = db.Column(db.String(255), index=True, nullable=False)
    foods = db.relationship('FoodsInPortions', backref='portion', lazy=False)

    def __repr__(self):
        return '<Title {}>'.format(self.title)


class FoodsInPortions(db.Model):
    """
    This table links the portion id to the amount of food that is saved in that portion, and it's id
    """
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    portion_id = db.Column(db.Integer, db.ForeignKey('portion.id'), nullable=False)
    amount = db.Column(db.Integer)

    def __repr__(self):
        return '<Food {}>'.format(self.food_id) + '<Portion {}>'.format(self.portion_id) \
               + '<Amount {}>'.format(self.amount)
