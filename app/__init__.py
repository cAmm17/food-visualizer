from flask import Flask
from config import Config

# create and configure the app
app = Flask(__name__)
app.config.from_object(Config)
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
