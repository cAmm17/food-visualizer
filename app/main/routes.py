from flask import render_template, request, redirect, flash, url_for
from app import app, db
from flask_login import current_user, login_user, logout_user
import json
from helpers import *


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
