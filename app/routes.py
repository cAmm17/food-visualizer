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
    return render_template('index.html', available_foods=available_foods)


@app.route('/addFood', methods=['POST'])
def addFood():
    strippedFoodName = request.form['food'].strip()
    # add database call here once it's setup, for now just test data
    return addFoodModel(strippedFoodName)


@app.route('/selectAddedFood', methods=['POST'])
def selectAddedFood():
    # add database call here when they are set up
    strippedFoodName = request.form['food'].strip()
    processed_selected = json.loads(request.form['allSelected'])
    return processNutritionInfo(strippedFoodName, foods_to_select, processed_selected)
