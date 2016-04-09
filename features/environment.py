import main
from main import app, address
from selenium import webdriver
from models import *
import threading


def before_all(context):
    app.config.from_object('config.TestingConfig')
    # context.client = app.test_client()
    context.server = main
    context.address = address
    context.thread = threading.Thread(target=context.server.serve_forever)
    context.thread.start()  # start flask app server
    context.browser = webdriver.Firefox()
    context.address = address
    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
        db.session.add(User('Sathwik', 'Singari', 'singarisathwik007@gmail.com', 'dm08b048'))
        db.session.add(User('Bilbo', 'Baggins', 'bbaggins@lotr.com', 'bilbobaggins'))
        db.session.commit()


def after_all(context):
    context.browser.get(context.address + "/shutdown")  # shut down flask app server
    context.thread.join()
    context.browser.quit()
    with app.app_context():
        db.session.remove()
        db.drop_all()

