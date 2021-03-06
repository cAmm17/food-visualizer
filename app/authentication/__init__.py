"""
Name: Courtney Amm
File: authentication/__init__.py

This file initiates the authentication blueprint for user logins and registration.

"""
from flask import Blueprint

bp = Blueprint('authentication', __name__, template_folder='templates')

from app.authentication import routes, forms
