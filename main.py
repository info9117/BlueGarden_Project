from flask import Flask, render_template, url_for, request, redirect, session, flash, send_from_directory, abort
from functools import wraps
from controllers import ProduceController
from models import *
from controllers.userController import UserController as userController
from controllers.farmController import FarmController as farmController
from shared import db

# Creating application object
app = Flask(__name__)
host = "http://localhost"
port = "5000"
address = host + ':' + port

# Setting app configuration
app.config.from_object('config.DevelopmentConfig')

# Creating SQLAlchemy Object
db.init_app(app)
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
            redirect_url = request.url
            return redirect(url_for('login', redirect=redirect_url))

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
    
@app.route('/addcrop',methods=['GET', 'POST'])
@login_required
def addcrop():
    return userController.addcrop()

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
    
@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/browse')
@login_required
def browse():
    return render_template('browse.html')


@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    return farmController.farms_view()


@app.route('/farm/<int:farm_id>/produce/add', methods=['GET', 'POST'])
@login_required
def add_produce_to_farm(farm_id):
    return ProduceController.add_produce(farm_id, app.config['UPLOAD_FOLDER'])


@app.route('/uploads/<int:farm_id>/<filename>')
def uploaded_image(farm_id, filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + 'produce/' + str(farm_id),
                               filename)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/shutdown')
def shutdown():
    shutdown_server()


if __name__ == '__main__':
    serve_forever()
