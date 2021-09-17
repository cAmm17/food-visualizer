"""
Author: Courtney Amm
File Description: This file holds all routing functions used to interface between
the client side and the backend server

"""

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
    init_foods = {}
    if current_user.is_authenticated:
        usernm = current_user.username
    else:
        usernm = ""
    return render_template('index.html', available_foods=available_foods,
                           initial_foods=init_foods, logged_in=current_user.is_authenticated,
                           username=usernm)


@app.route('/addFood', methods=['POST'])
def addFood():
    stripped_food_name = request.form['food'].strip()
    stripped_food_name = stripped_food_name.replace(" ", "_")
    return jsonify(addFoodModel(stripped_food_name))


@app.route('/selectAddedFood', methods=['POST'])
def selectAddedFood():
    stripped_food_name = request.form['food'].strip()
    stripped_food_name = stripped_food_name.replace(" ", "_")
    print(stripped_food_name)
    processed_selected = json.loads(request.form['allSelected'])
    return jsonify(processNutritionInfo(stripped_food_name, processed_selected))


@app.route('/save_portion', methods=['POST', 'GET'])
def save_portion():
    if current_user.is_authenticated:
        processed_selected = json.loads(request.form['allSelected'])
        saveNewPortion(request.form['portion_title'], request.form['portion_notes'],
                       processed_selected)
        flash("Portion has been successfully saved!")
    return


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


@app.route('/saved_portions')
def saved_portions():
    if current_user.is_authenticated:
        cur_user_portions = loadUsersPortions()
        usernm = current_user.username
        return render_template('saved-portions.html', portions=cur_user_portions, username=usernm)
    flash('You must be logged in to access this page')
    return redirect(url_for('login'))


@app.route('/saved_portions/<int:portion_id>')
def load_saved_portion(portion_id):
    init_foods = loadPortionFoods(portion_id)
    foods = Food.query.all()
    available_foods = {food.food_name for food in foods}
    if current_user.is_authenticated:
        usernm = current_user.username
    else:
        usernm = ""
    for food in init_foods:
        models = addFoodModel(food)
        init_foods[food] = {'amount': init_foods[food], 'modelPath': models['newModelPath'],
                            'collisionRadius': models['newCollisionRadius']}
    return render_template('index.html', available_foods=available_foods,
                           initial_foods=init_foods, logged_in=current_user.is_authenticated,
                           username=usernm)
