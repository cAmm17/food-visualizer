import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """This class sets up the configuration for the Flask server"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-ultra-secret-24SDF'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
