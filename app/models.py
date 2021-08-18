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

def processNutritionInfo(foodName, foods_info, selected_amounts):
    """Takes the inputed name and returns the nutritional info. If the info is all, then it
    adds up the nutritional info of all selected foods."""
    try:
        if (foodName == 'All'):
            allFoods = {'calories' : 0.0, 'fat' : 0.0, 'carbohydrates': 0.0, 'protein': 0.0 }
            for food in selected_amounts:
                #db call here
                if food != 'All':
                    amount = selected_amounts[food]
                    allFoods['calories'] += float(foods_info['calories']) * amount
                    allFoods['fat'] += float(foods_info['fat']) * amount
                    allFoods['carbohydrates'] += float(foods_info['carbohydrates']) * amount
                    allFoods['protein'] += float(foods_info['protein']) * amount

            return jsonify({'name': 'All Foods In Scene', 'calories' : str(allFoods['calories']),
                            'fat' : str(allFoods['fat']),
                            'carbohydrates': str(allFoods['carbohydrates']),
                            'protein' : str(allFoods['protein'])})
        else:
            #database call here
            amount = selected_amounts[foodName]
            totalFat = float(foods_info[foodName]['fat']) * amount
            totalCals = float(foods_info[foodName]['calories']) * amount
            totalCarbs = float(foods_info[foodName]['carbohydrates']) * amount
            totalProtein = float(foods_info[foodName]['protein']) * amount

            return jsonify({'name': foodName, 'calories': totalCals,
                            'fat': totalFat,
                            'carbohydrates': totalCarbs,
                            'protein': totalProtein})

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
