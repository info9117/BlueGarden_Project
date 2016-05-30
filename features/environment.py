import main
from main import app
from selenium import webdriver
from shared import db
from models import *
import threading


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
        db.session.add(User('Sathwik', 'Singari', 'singarisathwik007@gmail.com', 'dm08b048'))
        db.session.add(User('Bilbo', 'Baggins', 'bbaggins@lotr.com', 'bilbobaggins'))
        User.query.get(1).set_user_farmer()
        db.session.add(User('Billy', 'Bogan','email@email.com','password'))
        db.session.add(Unit('Kg'))
        db.session.add(Unit('gm'))
        db.session.add(Unit('l'))
        db.session.add(Unit('ml'))
        db.session.flush()

        db.session.add(Address('123 Hill Rd', None, 'Sydney', 'NSW', 'Australia', 2010))
        db.session.add(Address('126 Hill Rd', None, 'Sydney', 'NSW', 'Australia', 2010))
        db.session.add(Farm('Shire Farms', 1))
        db.session.add(Farm('Mordor Farms', 2))

        #db.session.add(Image('eggplant.jpg', 'produce/1/eggplant.jpeg'))
        #db.session.add(Produce('Eggplant', 'Sweet organic eggplants', 'Vegetable', 1, 1))
        #db.session.add(Price(1, 1, 4.35))
        #db.session.add(Price(1, 2, 2.8))

        db.session.add(Produce('corn', 'vegetable', 'tasty', 1, 1))
        db.session.add(Produce('milk', 'dairy', 'yum', 2, 2))
        db.session.flush()
        db.session.add(Price(1, 1, 2.2))
        db.session.add(Price(2, 1, 4.4))
        db.session.add(RecentProduce(1, 1))
        db.session.flush()
        db.session.add(Works(1, 1))
        db.session.add(Works(1, 2))
        db.session.add(Works(4,1))
        db.session.flush()
        db.session.add(User('Joe', 'Farmer', 'farmer_j01@gmail.com', 'louise1993'))
        #db.session.add(Works(4, 1))
        db.session.add(Field('west block', 'Shire Farms', 1))
        db.session.add(Resource('fertiliser', 1))

        db.session.commit()



def after_all(context):
    context.browser.get(context.address + "/shutdown")  # shut down flask app server
    context.thread.join()
    context.browser.quit()
    with app.app_context():
        db.session.remove()
        db.drop_all()

