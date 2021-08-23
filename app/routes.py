from flask import render_template, request, redirect, flash, url_for
from app import app, db
from flask_login import current_user, login_user, logout_user
import json
from .models import *
from .forms import *


@app.route('/')
@app.route('/index')
def index():
    foods = Food.query.all()
    available_foods = {food.food_name for food in foods}
    for food in available_foods:
        app.logger.error(food + "\n")
    return render_template('index.html', available_foods=available_foods, logged_in=False)


@app.route('/addFood', methods=['POST'])
def addFood():
    stripped_food_name = request.form['food'].strip()
    return addFoodModel(stripped_food_name)


@app.route('/selectAddedFood', methods=['POST'])
def selectAddedFood():
    stripped_food_name = request.form['food'].strip()
    processed_selected = json.loads(request.form['allSelected'])
    return processNutritionInfo(stripped_food_name, processed_selected)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    This route leads to the login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    log_form = LoginForm()
    if log_form.validate_on_submit():
        user = User.query.filter_by(username=log_form.username.data).first()
        if user is None or not user.check_password(log_form.password.form_data):
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
        user.set_password(reg_form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered your new account.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=reg_form)
