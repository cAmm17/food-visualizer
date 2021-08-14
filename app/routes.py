from flask import jsonify, render_template, request
from app import app
from models import *

available_foods = [{'name': 'Banana', 'modelPath': 'models/banana_whole.glb',
                    'collisionRadius': '3'},
                   {'name': 'Blueberries', 'modelPath': 'models/blueberry.glb',
                    'collisionRadius': '1'}]
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
    return render_template('index.html', available_foods=available_foods,
                           selected_foods=selected_foods,
                           selected_food=foods_to_select[selected_food])


@app.route('/addFood', methods=['POST'])
def addFood():
    strippedFoodName = request.form['food'].strip()
    # add database call here once it's setup, for now just test data
    return addFoodModel(strippedFoodName)

@app.route('/select_added_food', methods=['POST'])
def selectAddedFood():
    # add database call here when they are set up
    strippedFoodName = request.form['food'].strip()
    return processNutritionInfo(strippedFoodName, selected_foods)
