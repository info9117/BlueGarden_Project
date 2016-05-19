import main
from main import app
from selenium import webdriver
from shared import db
from models import *
import threading
from models.user import *


def before_all(context):
    app.config.from_object('config.TestingConfig')
    # context.client = app.test_client()
    context.server = main
    context.address = main.address
    context.thread = threading.Thread(target=context.server.serve_forever)
    context.thread.start()  # start flask app server
    context.browser = webdriver.Firefox()
    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
        user1 = User('Sathwik', 'Singari', 'singarisathwik007@gmail.com', 'dm08b048')
        user1.set_user_farmer()
        db.session.add(user1)
        db.session.add(User('Bilbo', 'Baggins', 'bbaggins@lotr.com', 'bilbobaggins'))
        db.session.add(Unit('Kg'))
        db.session.add(Unit('gm'))
        db.session.add(Unit('l'))
        db.session.add(Unit('ml'))
        db.session.flush()
        db.session.add(Address('123 Hill Rd', None, 'Sydney', 'NSW', 'Australia', 2010))
        db.session.add(Address('126 Hill Rd', None, 'Sydney', 'NSW', 'Australia', 2010))
        db.session.flush()
        db.session.add(Farm('Shire Farms', 1))
        db.session.add(Farm('Mordor Farms', 2))
        db.session.flush()
        db.session.add(Works(1, 1))
        db.session.add(Works(1, 2))
        db.session.flush()
        db.session.add(User('Joe', 'Farmer', 'farmer_j01@gmail.com', 'louise1993'))
        db.session.commit()


def after_all(context):
    context.browser.get(context.address + "/shutdown")  # shut down flask app server
    context.thread.join()
    context.browser.quit()
    with app.app_context():
        db.session.remove()
        db.drop_all()

