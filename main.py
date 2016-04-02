from flask import Flask, render_template, url_for, request, redirect, session, flash
from functools import wraps
from models import *

# Creating application object
app = Flask(__name__)

# Setting app configuration
app.config.from_object('config.DevelopmentConfig')

# Creating SQLAlchemy Object
from shared import db
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
    errors = []
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        if not email:
            errors.append('Email Id cannot be empty')
        else:
            user = User.query.filter_by(email=email).first()
        if not password:
            errors.append('Password cannot be empty')
        else:
            if user:
                if not user.check_password(password):
                    errors.append("Email Id/Password do not match")
        if not errors:
            session['logged_in'] = True
            session['email'] = email
            session['firstname'] = user.first_name
            session['lastname'] = user.last_name
            return redirect(url_for('dashboard'))
    return render_template("login.html", errors=errors)


@app.route("/register", methods=['GET', 'POST'])
def register():
    errors = []
    if request.method == 'POST':
        first_name = request.form.get('firstname', '')
        last_name = request.form.get('lastname', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        if not first_name:
            errors.append('First Name cannot be empty')
        if not last_name:
                errors.append('Last Name cannot be empty')
        if not email:
            errors.append('Email Id cannot be empty')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                errors.append("Email Id already exists")
        if not password:
            errors.append('Password cannot be empty')
        if not errors:
            user = User(first_name, last_name, email, password)
            db.session.add(user)
            db.session.commit()
            session['logged_in'] = True
            session['email'] = user.email
            session['firstname'] = user.first_name
            session['lastname'] = user.last_name
            return redirect(url_for('dashboard'))
    return render_template("register.html", errors=errors)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('firstname', None)
    session.pop('lastname', None)
    flash('You successfully logged out', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run()
