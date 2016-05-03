from flask import request, render_template, session, redirect, url_for, flash

from models.user import *
from models.crop import *
from models.farm import *



class UserController:

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def logout():
        session.pop('logged_in', None)
        session.pop('email', None)
        session.pop('firstname', None)
        session.pop('lastname', None)
        flash('You successfully logged out', 'success')
        return redirect(url_for('login'))
        
        
        
    @staticmethod
    def addcrop():
        errors = []
        if request.method == 'POST':
            id = request.form.get('id', '')
            crop_name = request.form.get('cropname', '')
            grow_state = request.form.get('growstate', '')
            farm_id = request.form.get('farmid', '')
            crop = Crop(id, crop_name, grow_state, farm_id)
            db.session.add(crop)
            db.session.commit()
            flash('You success added crop')
        return render_template("addcrop.html", errors=errors)
        
        
    '''@staticmethod
    def viewcrop():
        errors = []
        if '''
 
        
