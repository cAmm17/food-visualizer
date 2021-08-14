from flask import jsonify, request
import logging
from app import app

available_foods_dict = {'Banana': {'modelPath': 'models/banana_whole.glb',
                                   'collisionRadius': '3'},
                        'Blueberries': {'modelPath': 'models/blueberry.glb',
                                        'collisionRadius': '1'}}

foods_to_select = {'Banana': {'name': 'Banana',
                              'calories': '80',
                              'fat': '1.2',
                              'protein': '1.0',
                              'carbohydrates': '10.0'},
                   'Blueberries': {
                       'name': 'Blueberries',
                       'calories': '3',
                       'fat': '0.1',
                       'protein': '0.1',
                       'carbohydrates': '1'
                   }}

def processNutritionInfo(foodName, selected_foods):
    """Takes the inputed name and returns the nutritional info. If the info is all, then it
    adds up the nutritional info of all selected foods."""
    try:
        if (foodName == 'All'):
            allFoods = {'calories' : 0.0, 'fat' : 0.0, 'carbohydrates': 0.0, 'protein': 0.0 }
            for food in selected_foods:
                #db call here
                allFoods['calories'] += float(food['calories'])
                allFoods['fat'] += float(food['fat'])
                allFoods['carbohydrates'] += float(food['carbohydrates'])
                allFoods['protein'] += float(food['protein'])

            return jsonify({'name': 'All Foods In Scene', 'calories' : str(allFoods['calories']),
                            'fat' : str(allFoods['fat']),
                            'carbohydrates': str(allFoods['carbohydrates']),
                            'protein' : str(allFoods['protein'])})
        else:
            #database call here
            return jsonify({'name': foodName, 'calories': foods_to_select[foodName]['calories'],
                            'fat': foods_to_select[foodName]['fat'],
                            'carbohydrates': foods_to_select[foodName]['carbohydrates'],
                            'protein': foods_to_select[foodName]['protein']})

    except (KeyError):
        app.logger.error('ERROR :: Could not find nutritional information for selected foods')
        return jsonify({'name': 'Not Found', 'calories' : '0.0', 'fat' : '0.0',
                        'carbohydrates' : '0.0', 'protein' : '0.0'})

def addFoodModel(foodName):
    """Takes the selected food and returns it's model path and the collision radius for that
    model. On the client side, the selected food is also added to a list of selected foods"""
    return jsonify({'newModelPath': available_foods_dict[foodName]['modelPath'],
                    'newCollisionRadius': available_foods_dict[foodName][
                        'collisionRadius']})
