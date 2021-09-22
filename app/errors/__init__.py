"""
Author: Courtney Amm
File: errors/__init__.py

This file initiates the errors blueprint
"""
from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
