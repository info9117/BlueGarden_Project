from flask import Flask, render_template, url_for, request, redirect, session, flash, send_from_directory, abort
import stripe
from functools import wraps
from controllers import ProduceController, CheckoutController
from werkzeug.security import safe_join
from controllers.userController import UserController
from models import *
from controllers.userController import UserController as userController
from controllers.farmController import FarmController as farmController
from controllers.fieldController import FieldController as fieldController
from controllers.cropController import CropController as cropController
from controllers.templateController import TemplateController as templateController
from controllers.resourcelistController import ResourceController as resourceController
from controllers.feedbackController import FeedbackController
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


# keys for payment
stripe_keys = {
    'secret_key': 'sk_test_BQokikJOvBiI2HlWgH4olfQ2',
    'publishable_key': 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'
}
stripe.api_key = stripe_keys['secret_key']


# Login Required wrap
def login_required(function):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        if session.get('logged_in', False):
            return function(*args, **kwargs)
        else:
            flash('Please login to view this page', 'error')
            redirect_url = wrapped_function.__name__
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


@app.route('/logout')
def logout():
    return userController.logout()


@app.route('/addcrop', methods=['GET', 'POST'])
@login_required
def addcrop():
    return userController.addcrop()


@app.route('/change_state/<int:crop_id>', methods=['GET', 'POST'])
@login_required
def change_state(crop_id):
    return cropController.change_state(crop_id)


@app.route('/dashboard')
@login_required
def dashboard():
    return userController.show_dashboard()


@app.route('/search/produce', defaults={'page': 1})
@app.route('/search/produce/page/<int:page>')
def browse_produce(page):
    return ProduceController.browse_produce(page)


@app.route('/checkout/<int:item_id>', methods=['POST', 'GET'])
def checkout(item_id):
    return CheckoutController.checkout(item_id)


@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    return farmController.add_farm()


@app.route('/activity/<int:process_id>', methods=['GET', 'POST'])
@login_required
def activity(process_id):
    return farmController.activity(process_id)


@app.route('/field', methods=['GET', 'POST'])
@login_required
def field():
    return fieldController.addField()


@app.route('/addresource', methods=['GET', 'POST'])
@login_required
def resource():
    return resourceController.add_resource()


@app.route('/farm/<int:farm_id>/produce/add', methods=['GET', 'POST'])
@login_required
def add_produce_to_farm(farm_id):
    return ProduceController.add_produce(farm_id, app.config['UPLOAD_FOLDER'])


@app.route('/produce/<int:produce_id>', methods=['POST', 'GET'])
def view_produce(produce_id):
    return ProduceController.view_produce(produce_id)


@app.route('/uploads/<int:farm_id>/<filename>', )
def uploaded_image(farm_id, filename):
    print(safe_join(app.config['UPLOAD_FOLDER'] + 'produce/' + str(farm_id), filename))
    return send_from_directory(app.config['UPLOAD_FOLDER'] + 'produce/' + str(farm_id) + '/',
                               filename)


@app.route('/process', methods=['GET', 'POST'])
@login_required
def process():
    return templateController.add_process()


@app.route('/active_process/<process_or_crop>/<int:id>', methods=['GET', 'POST'])
@login_required
def active_process(process_or_crop, id):
    return farmController.active_process(process_or_crop, id)


@app.route('/activity/<int:process_id>/add', methods=['GET', 'POST'])
@login_required
def add_activity_to_process(process_id):
    return farmController.linkToActivity(process_id)


def url_for_browse_produce(page):
    args = dict(list(request.view_args.items()) + list(request.args.to_dict().items()))
    args['page'] = page
    return url_for('browse_produce', **args)


app.jinja_env.globals['url_for_browse_produce'] = url_for_browse_produce


@app.route('/purchase/<int:checkId>')
def reference(checkId):
    check1 = Check.query.get(checkId)
    return render_template('reference.html', key=stripe_keys['publishable_key'], check=check1)


@app.route('/charge', methods=['POST'])
def charge():
    amount = 500

    # customer = stripe.Customer.create(
    #       email=request.form['stripeEmail'],
    #       card=request.form['stripeToken']
    #     )

    # charge = stripe.Charge.create(
    #       customer=customer.id,
    #       amount=amount,
    #       currency='AUD',
    #       description='Flask Charge'
    #   )
    return render_template('charge.html', amount=amount)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.route('/shutdown')
def shutdown():
    shutdown_server()


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    return FeedbackController.feedback()


if __name__ == '__main__':
    serve_forever()
