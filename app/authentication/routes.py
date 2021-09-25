"""
Author: Courtney Amm
File: authentication/routes.py

This file contains the routes for the user authentication system blueprint.

"""
from flask import render_template, redirect, flash, url_for
from app import db
from app.authentication import bp
from flask_login import current_user, login_user, logout_user
from .forms import *


@bp.route('/login', methods=['POST', 'GET'])
def login():
    """
    If there is already a user logged in, this route redirects the user to the index page. Otherwise
    it send the user to the login page and processes the login form once it is entered. If the login
    info is correct, the user is logged in, otherwise an error is flashed.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    log_form = LoginForm()
    if log_form.validate_on_submit():
        user = User.query.filter_by(username=log_form.username.data).first()
        if user is None or not user.check_password(log_form.password.data):
            flash("Username or Password incorrect")
            return redirect(url_for('authentication.login'))
        login_user(user, remember=log_form.remember_me.data)
        return redirect("/index")
    return render_template('login.html', title="Sign in", form=log_form)


@bp.route('/logout')
def logout():
    """
    The route logs out the current user.
    """
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['POST', 'GET'])
def register():
    """
    If there is already a user logged in, this route redirects the user to the index page. Otherwise
    it send the user to the registration page and processes the registration form
    once it is entered.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        user = User()
        user.username = reg_form.username.data
        user.email = reg_form.email.data
        user.set_password(reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered your new account.')
        return redirect(url_for('authentication.login'))
    return render_template('register.html', title='Register', form=reg_form)
