"""
Name: Courtney Amm
File: main/helpers.py

This file contains the helper functions for the main application functionality's routes.

"""
from flask_login import current_user
from flask import current_app
from ..models import *


def processNutritionInfo(foodName, selected_amounts):
    """
    Takes the inputed name and returns the nutritional info. If the info is all, then it
    adds up the nutritional info of all selected foods.
    """
    try:
        if foodName == 'All':
            all_foods = {'calories': 0.0, 'fat': 0.0, 'carbohydrates': 0.0, 'protein': 0.0}
            for food in selected_amounts:
                # db call here
                if food != 'All':
                    amount = selected_amounts[food]
                    f = Food.query.filter_by(food_name=food).first_or_404()
                    all_foods['calories'] += f.calories * amount
                    all_foods['fat'] += f.fat * amount
                    all_foods['carbohydrates'] += f.carbohydrates * amount
                    all_foods['protein'] += f.protein * amount

            return {'name': 'All Foods In Scene', 'calories': str(all_foods['calories']),
                    'fat': str(all_foods['fat']),
                    'carbohydrates': str(all_foods['carbohydrates']),
                    'protein': str(all_foods['protein'])}
        else:
            amount = selected_amounts[foodName]
            f = Food.query.filter_by(food_name=foodName).first_or_404()
            total_fat = f.fat * amount
            total_cals = f.calories * amount
            total_carbs = f.carbohydrates * amount
            total_protein = f.protein * amount

            return {'name': foodName, 'calories': total_cals,
                    'fat': total_fat,
                    'carbohydrates': total_carbs,
                    'protein': total_protein}

    except (KeyError):
        current_app.logger.error('ERROR :: Could not find nutritional information for selected foods')
        current_app.logger.error('Food Name: ' + foodName + " selected_amounts" + str(selected_amounts))
        return {'name': 'Not Found', 'calories': '0.0', 'fat': '0.0',
                'carbohydrates': '0.0', 'protein': '0.0'}


def addFoodModel(foodName):
    """
    Takes the selected food and returns it's model path and the collision radius for that
    model. On the client side, the selected food is also added to a list of selected foods.
    """
    f = Food.query.filter_by(food_name=foodName).first_or_404()
    return {'newModelPath': f.model_path,
            'newCollisionRadius': f.collision_radius}


def saveNewPortion(title, notes, selected_foods):
    """
    Takes the currently selected portions and saves it to the database for that user
    to reopen later.
    """
    p = Portion()
    p.title = title
    p.notes = notes
    p.user_id = User.query.filter_by(username=current_user.username).first().id
    db.session.add(p)
    for food in selected_foods:
        if food != "All":
            f = FoodsInPortions()
            underscore_food = food.replace(" ", "_")
            f.food_id = Food.query.filter_by(food_name=underscore_food).first().id
            f.portion_id = p.id
            f.amount = selected_foods[food]
            db.session.add(f)
    db.session.commit()
    return


def loadUsersPortions():
    """
    Loads all of a user's saved portions from the database and stores them in a dictionary.
    """
    if current_user.is_authenticated:
        all_user_portions = {}
        user_portions = Portion.query.filter_by(user_id=current_user.id).all()
        print(current_user.id)
        if user_portions is not None:
            for port in user_portions:
                all_user_portions[port.id] = loadPortion(port.id)
                all_user_portions[port.id]['title'] = port.title
                all_user_portions[port.id]['notes'] = port.notes
                all_user_portions[port.id]['timestamp'] = port.timestamp
        return all_user_portions


def loadPortion(p_id):
    """
    Helper funtion for loadUserPortions. Loads in the foods and nutritional info for an
    individual portion
    """
    portion = {'foods': loadPortionFoods(p_id)}
    nutrition = processNutritionInfo('All', portion['foods'])
    for key in nutrition:
        if key != 'name':
            portion[key] = nutrition[key]
    return portion


def loadPortionFoods(p_id):
    """
    Returns a list of foods in the given portion. Helper function for loadPortion()
    """
    foods_in_portion = {}
    temp_foods = FoodsInPortions.query.filter_by(portion_id=p_id).all()
    for food in temp_foods:
        f = Food.query.filter_by(id=food.food_id).first()
        foods_in_portion[f.food_name] = food.amount
    return foods_in_portion
