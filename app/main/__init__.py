"""
Author: Courtney Amm
File: main/__init__.py

This file initializes the main Blueprint containing the main functionality of the application.

"""
from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import helpers, routes
