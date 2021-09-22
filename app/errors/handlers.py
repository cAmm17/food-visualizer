"""
Author: Courtney Amm
File: errors/handlers.py

This file is part of the errors blueprint. It contains the error handlers for 404 and 500 errors,
rendering the 404 or 500 error page to the user when an error occurs.
"""
from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Renders a 404 error page to the user when a 404 error is encountered.
    """
    return render_template('404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Renders a 500 error page to the user when a 500 error is encountered.
    """
    db.session.rollback()
    return render_template('500.html'), 500
