"""
Author: Courtney Amm
File: portion_visualizer.py

This file initializes and launches the web app

"""
from app import create_app, db
from app.models import Food, User, Portion, FoodsInPortions

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """
    This function creates a preconfigured Flask shell context, which makes it easy to add items to
    the database as all needed modules are pre-imported.
    """
    return {'db': db, 'Food': Food, 'User': User, 'Portion': Portion,
            'FoodsInPortions': FoodsInPortions}
