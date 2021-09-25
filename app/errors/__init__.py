"""
Author: Courtney Amm
File: errors/__init__.py

This file initiates the errors blueprint
"""
from flask import Blueprint

bp = Blueprint('errors', __name__, template_folder='templates')

from app.errors import handlers
