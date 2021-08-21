from flask import render_template, request
from app import app, db
import json
from .models import *


available_foods_dict = {'Banana': {'modelPath': 'models/banana_whole.glb',
                                   'collisionRadius': '3'},
                        'Blueberries': {'modelPath': 'models/blueberry.glb',
                                      'collisionRadius': '1'}}
selected_foods={}
selected_food = "Banana"
foods_to_select = {'Banana' : {'name': 'Banana',
                 'calories': '80',
                 'fat': '1.2',
                 'protein': '1.0',
                 'carbohydrates': '10.0'},
                   'Blueberries' : {
                       'name': 'Blueberries',
                       'calories': '3',
                       'fat': '0.1',
                       'protein': '0.1',
                       'carbohydrates': '1'
                   }}


@app.route('/')
@app.route('/index')
def index():
    foods = Food.query.all()
    available_foods = {food.food_name for food in foods}
    for food in available_foods:
        app.logger.error(food + "\n")
    return render_template('index.html', available_foods=available_foods)


@app.route('/addFood', methods=['POST'])
def addFood():
    stripped_food_name = request.form['food'].strip()
    return addFoodModel(stripped_food_name)


@app.route('/selectAddedFood', methods=['POST'])
def selectAddedFood():
    stripped_food_name = request.form['food'].strip()
    processed_selected = json.loads(request.form['allSelected'])
    return processNutritionInfo(stripped_food_name, foods_to_select, processed_selected)
