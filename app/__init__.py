from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# create and configure the app
app = Flask(__name__)
app.config.from_object(Config)
# create the database itself, using SQLalchemy
db = SQLAlchemy(app)
# Migrate is a tool to help migrate databases as the application's needs change
mig = Migrate(app, db)
login = LoginManager(app)




from app import routes
