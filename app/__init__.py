from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# create and configure the app
app = Flask(__name__)
app.config.from_object(Config)
# create the database itself, using SQLalchemy
db = SQLAlchemy(app)
# Migrate is a tool to help migrate databases as the application's needs change
mig = Migrate(app, db)

@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers["Cache-Control"] = "no-cache, no-store"  # HTTP 1.1.
    return response
# app.config.from_mapping(
#   SECRET_KEY='dev',
#  DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
# )


# ensure the instance folder exists
# try:
#   os.makedirs(app.instance_path)
# except OSError:
#   pass

from app import routes

# from . import db
# db.init_app(app)
