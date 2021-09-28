"""
Author: Courtney Amm
File: __init__.py

This file initializes the web app using Flask's Application Factory pattern.

"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# create the database itself, using SQLalchemy
db = SQLAlchemy()
# Migrate is a tool to help migrate databases as the application's needs change
mig = Migrate(db)
login = LoginManager()


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mig.init_app(app, db)
    login.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.authentication import bp as authentication_bp
    app.register_blueprint(authentication_bp, url_prefix='/authentication')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
