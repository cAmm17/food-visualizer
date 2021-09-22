from flask import render_template, request, redirect, flash, url_for
from app import app, db
from flask_login import current_user, login_user, logout_user
import json
from .forms import *


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    This route leads to the login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    log_form = LoginForm()
    if log_form.validate_on_submit():
        user = User.query.filter_by(username=log_form.username.data).first()
        if user is None or not user.check_password(log_form.password.data):
            flash("Username or Password incorrect")
            return redirect(url_for('login'))
        login_user(user, remember=log_form.remember_me.data)
        return redirect("/index")
    return render_template('login.html', title="Sign in", form=log_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        user = User()
        user.username = reg_form.username.data
        user.email = reg_form.email.data
        user.set_password(reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered your new account.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=reg_form)
