from flask import jsonify, render_template, request
from app import app

available_foods = [{'name': 'Banana', 'modelPath': 'models/banana_whole.glb',
                    'collisionRadius': '3'},
                   {'name': 'Blueberry', 'modelPath': 'models/blueberry.glb',
                    'collisionRadius': '1'}]
available_foods_dict = {'Banana': {'modelPath': 'models/banana_whole.glb',
                                   'collisionRadius': '3'},
                        'Blueberry': {'modelPath': 'models/blueberry.glb',
                                      'collisionRadius': '1'}}
selected_foods = [{'name': 'Apple'}, {'name': 'Pear'}]
selected_food = {'name': 'Apple',
                 'calories': '80',
                 'fat': '1.2',
                 'protein': '1.0',
                 'carbohydrates': '10.0'}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', available_foods=available_foods,
                           selected_foods=selected_foods, selected_food=selected_food)


@app.route('/addFood', methods=['POST'])
def addFood():
    strippedFoodName = request.form['food'].strip()
    # add database call here once it's setup, for now just test data
    return jsonify({'newModelPath': available_foods_dict[strippedFoodName]['modelPath'],
                    'newCollisionRadius': available_foods_dict[strippedFoodName]['collisionRadius']})
