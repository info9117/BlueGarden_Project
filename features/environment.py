from main import app
from models import *


def before_all(context):
    app.config.from_object('config.TestingConfig')
    context.client = app.test_client()
    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
        db.session.add(User('Sathwik', 'Singari', 'singarisathwik007@gmail.com', 'dm08b048'))
        db.session.add(User('Bilbo', 'Baggins', 'bbaggins@lotr.com', 'bilbobaggins'))
        db.session.commit()


def after_all(context):
    with app.app_context():
        db.session.remove()
        db.drop_all()

