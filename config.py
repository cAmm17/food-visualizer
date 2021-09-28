"""
Author: Courtney Amm
File: config.py

This file holds the configuration data for environent variables needed by flask and the SQL
database.
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """This class sets up the configuration for the Flask server"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or '87ab3d95fa3ec450185d6f3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
