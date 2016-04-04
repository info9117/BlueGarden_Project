from flask import Flask, render_template, url_for, request, redirect, session, flash
from functools import wraps

from controllers.userController import UserController as userController
from models import *
from shared import db

# Creating application object
app = Flask(__name__)

# Setting app configuration
app.config.from_object('config.DevelopmentConfig')

# Creating SQLAlchemy Object
db.init_app(app)


# Login Required wrap
def login_required(function):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        if session.get('logged_in', False):
            return function(*args, **kwargs)
        else:
            flash('Please login to view this page', 'error')
            next_page = request.url
            return redirect(url_for('login', next_page=next_page))
    return wrapped_function


@app.route("/")
def index():
    if session.get('logged_in', False):
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    return userController.login()


@app.route("/register", methods=['GET', 'POST'])
def register():
    return userController.register()


@app.route('/logout')
def logout():
    return userController.logout()


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
