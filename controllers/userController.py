from flask import request, render_template, session, redirect, url_for, flash

from models.user import *
<<<<<<< HEAD
=======
from models.crop import *
from models.address import *
from models.recent_produce import RecentProduce
>>>>>>> test-sprint-2


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
<<<<<<< HEAD
=======

                else:
                    errors.append("User doesn't exist")
>>>>>>> test-sprint-2
            if not errors:
                session['logged_in'] = True
                session['email'] = email
                session['firstname'] = user.first_name
                session['lastname'] = user.last_name
                if request.args.get('redirect'):
                    return redirect(request.args.get('redirect'))
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
            conf_pswd = request.form.get('confirm password', '')
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
            if conf_pswd != password:
                errors.append('Password mismatch! ')
            if not errors:
                user = User(first_name, last_name, email, password)
                db.session.add(user)
                db.session.commit()
<<<<<<< HEAD
                session['logged_in'] = True
                session['email'] = user.email
                session['firstname'] = user.first_name
                session['lastname'] = user.last_name
=======

                user.add_user_to_session()

>>>>>>> test-sprint-2
                return redirect(url_for('dashboard'))
        return render_template("register.html", errors=errors)

    @staticmethod
    def logout():
        session.pop('logged_in', None)
        session.pop('email', None)
        session.pop('firstname', None)
        session.pop('lastname', None)
        flash('You are successfully logged out', 'success')
        return redirect(url_for('login'))


    @staticmethod
    def addcrop():
        errors = []
        crop_m = []
        myfarm = []
        #user = User.query.get(User.query.filter_by(email=session['email']).first().id())
        #myfarms
        if request.method == 'POST':
            #if request.form['action']=="add crop":
            id = request.form.get('id', '')
            crop_name = request.form.get('cropname', '')
            grow_state = request.form.get('growstate', '')
            farm_id = request.form.get('farmid', '')
            crop = Crop(id, crop_name, grow_state, farm_id)
            db.session.add(crop)
            db.session.commit()
<<<<<<< HEAD
            flash('You have added crop successfully')
        return render_template("addcrop.html", errors=errors)
=======
            flash('You success added crop')
            


        
        
        crop_m=Crop.query.all()
            
        return render_template("addcrop.html",crop_m=crop_m,errors = errors)

    @staticmethod
    def show_dashboard():
        id = session.get("id")
        recently_viewed = RecentProduce.query.order_by(RecentProduce.id.desc()).filter_by(user_id=id).limit(4)
        return render_template('dashboard.html', items=recently_viewed)


>>>>>>> test-sprint-2
