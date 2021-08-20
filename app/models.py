from flask import jsonify, request
import logging
from datetime import datetime
from app import app, db

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
        if foodName == 'All':
            allFoods = {'calories': 0.0, 'fat': 0.0, 'carbohydrates': 0.0, 'protein': 0.0}
            for food in selected_amounts:
                # db call here
                if food != 'All':
                    amount = selected_amounts[food]
                    allFoods['calories'] += float(foods_info['calories']) * amount
                    allFoods['fat'] += float(foods_info['fat']) * amount
                    allFoods['carbohydrates'] += float(foods_info['carbohydrates']) * amount
                    allFoods['protein'] += float(foods_info['protein']) * amount

            return jsonify({'name': 'All Foods In Scene', 'calories': str(allFoods['calories']),
                            'fat': str(allFoods['fat']),
                            'carbohydrates': str(allFoods['carbohydrates']),
                            'protein': str(allFoods['protein'])})
        else:
            # database call here
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
        return jsonify({'name': 'Not Found', 'calories': '0.0', 'fat': '0.0',
                        'carbohydrates': '0.0', 'protein': '0.0'})


def addFoodModel(foodName):
    """Takes the selected food and returns it's model path and the collision radius for that
    model. On the client side, the selected food is also added to a list of selected foods"""
    f = Food.query.filter_by(food_name=foodName).first_or_404()
    return jsonify({'newModelPath': f.model_path,
                    'newCollisionRadius': f.collision_radius})


# Database Models ####################################################################

class Food(db.Model):
    """
    A database table representing each food item, including it's name, model path, and nutritional
    info
    """
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(64), index=True, unique=True)
    model_path = db.Column(db.String(120), index=True, unique=True)
    collision_radius = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Float, nullable=False)
    fiber = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    saturated_fat = db.Column(db.Float, nullable=False)
    trans_fat = db.Column(db.Float, nullable=False)
    monounsaturated_fat = db.Column(db.Float, nullable=False)
    polyunsaturated_fat = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    in_portions = db.relationship('FoodsInPortions', backref='food', lazy=True)

    def __repr__(self):
        """
        This function tells python how to "print" the class, which is helpful for debugging.
        In this case, it returns the foods name and model path.
        """
        return "<food {}>".format(self.food_name) + "<model_path {}".format(self.model_path)


class User(db.Model):
    """
    Database that stores users
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(64), index=True, nullable=False)
    portions = db.relationship('Portion', backref='user', lazy=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Portion(db.Model):
    """
    Database that stores each user's created potions
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.String(128), index=True, nullable=False)
    notes = db.Column(db.String(255), index=True, nullable=False)
    foods = db.relationship('FoodsInPortions', backref='portion', lazy=False)

    def __repr__(self):
        return '<Title {}>'.format(self.title)


class FoodsInPortions(db.Model):
    """
    This table links the portion id to the amount of food that is saved in that portion, and it's id
    """
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    portion_id = db.Column(db.Integer, db.ForeignKey('portion.id'), nullable=False)
    amount = db.Column(db.Integer)

    def __repr__(self):
        return '<Food {}>'.format(self.food_id) + '<Portion {}>'.format(self.portion_id) \
               + '<Amount {}>'.format(self.amount)
