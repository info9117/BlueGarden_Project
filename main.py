from flask import Flask, render_template, url_for, request, redirect, session, flash
from functools import wraps

from models import *

from controllers.userController import UserController as userController
from shared import db, mail

# Creating application object
app = Flask(__name__)
host = "http://localhost"
port = "5000"
address = host+':'+port

# Setting app configuration
app.config.from_object('config.DevelopmentConfig')

# Creating SQLAlchemy Object
db.init_app(app)
mail.init_app(app)
with app.app_context():
    db.create_all()

def serve_forever():
    app.run()


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with Werkzeug server")
    func()


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


@app.route("/resetpassword", methods=['GET','POST'])
def resetpassword():
    return userController.resetpassword()


@app.route("/resetpassword/<token>/<int:user_id>", methods=['GET', 'POST'])
def changepassword(token, user_id):
    return userController.changepassword(token,user_id)

@app.route("/resetdone", methods=['GET','POST'])
def resetdone():
    return userController.resetdone()


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


@app.route('/shutdown')
def shutdown():
    shutdown_server()


if __name__ == '__main__':
    serve_forever()
