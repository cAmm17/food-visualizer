from app import app, db
from app.models import Food, User, Portion, FoodsInPortions


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Food': Food, 'User': User, 'Portion': Portion,
            'FoodsInPortions': FoodsInPortions}


if __name__=='__main__':
    app.run()
