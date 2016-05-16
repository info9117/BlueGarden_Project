import os
from flask import Flask, render_template, url_for, request, redirect, session, flash, send_from_directory
from functools import wraps
from controllers.userController import UserController as userController
from shared import db, mail
from werkzeug.security import safe_join
from controllers.userController import UserController
from werkzeug.utils import secure_filename
import utilities
from models import *

# Creating application object
app = Flask(__name__)
host = "http://localhost"
port = "5000"
address = host + ':' + port

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
    return UserController.login()


@app.route("/register", methods=['GET', 'POST'])
def register():
    return UserController.register()


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
    return UserController.logout()


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/browse')
@login_required
def browse():
    return render_template('browse.html')


@app.route('/sell')
@login_required
def sell():
    return render_template('sell.html')


@app.route('/farm/<int:farm_id>/produce/add', methods=['GET', 'POST'])
@login_required
def add_produce_to_farm(farm_id):
    errors = []
    if request.method == 'POST':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        category = request.form.get('category', '')
        selected_units = request.form.get('units', '')
        prices = {}
        for unit in selected_units:
            prices[unit] = request.form.get('price-'+selected_units)
        file = request.files['prod_image']
        if not name:
            errors.append('Name cannot be empty')
        if not description:
            errors.append('Description cannot be empty')
        if not category:
            errors.append('Please choose a category for the produce')
        if not selected_units:
            errors.append('Please choose the units you wish to sell in')
        if len(prices) < len(selected_units):
            errors.append('Please enter the prices for the produce')
        if not file or not utilities.allowed_file(file.filename):
            errors.append("Please upload 'png', 'jpg', 'jpeg' or 'gif' image for produce")
        if not errors:
            directory = os.path.join(app.config['UPLOAD_FOLDER'], 'produce/' + str(farm_id) + '/')
            os.makedirs(os.path.dirname(directory), exist_ok=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(directory, filename))
            image = Image('produce/' + str(farm_id)+'/'+filename)
            db.session.add(image)
            produce = Produce(name, description, category, image.id)
            db.session.add(produce)
            for price in prices:
                db.session.add(Price(produce.id, price, prices[price]))
            db.session.commit()
            return 'Success'
    units = Unit.query.all()
    farm = Farm.query.get(farm_id)
    farm_address = Address.query.get(farm.address_id)
    return render_template('add_produce.html', units=units, farm=farm, address=farm_address, errors=errors)


@app.route('/produce/<int:produce_id>', methods=['POST', 'GET'])
def view_produce(produce_id):
    produce1 = Produce.query.get(produce_id)
    if request.method == 'POST':
        amount = request.form.get('amount')
        print('amount', type(amount))
        print('produce', type(produce1.prices[0].price))
        if amount:
            amount = request.form.get('amount', '')
            item1 = Item(produce1.prices[0].price, produce_id, amount)
            db.session.add(item1)
            db.session.commit()
            return render_template('view_produce.html', produce=produce1, total=item1.total)
        else:
            return render_template('view_produce.html', produce=produce1, total="wrong value")
    
    return render_template('view_produce.html', produce=produce1)


@app.route('/uploads/<int:farm_id>/<filename>')
def uploaded_image(farm_id, filename):
    print(safe_join(app.config['UPLOAD_FOLDER']+'produce/' + str(farm_id), filename))
    return send_from_directory(app.config['UPLOAD_FOLDER']+'produce/' + str(farm_id)+'/',
                               filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


def url_for_browse_produce(page):
    args = dict(list(request.view_args.items()) + list(request.args.to_dict().items()))
    args['page'] = page
    return url_for('browse_produce', **args)
app.jinja_env.globals['url_for_browse_produce'] = url_for_browse_produce


@app.route('/shutdown')
def shutdown():
    shutdown_server()


if __name__ == '__main__':
    serve_forever()
