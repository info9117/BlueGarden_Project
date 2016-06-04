from flask import request, render_template, session, redirect, url_for, flash

from models import PasswordResets
from models.user import *
from models.crop import *
from models.address import *
from models.recent_produce import RecentProduce
import datetime as DT
from shared import mail
from flask_mail import Message
import random


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
                else:
                    errors.append("User doesn't exist")
            if not errors:
                user.add_user_to_session()
                if request.args.get('redirect'):
                    return redirect(url_for(request.args.get('redirect')))
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
            conf_pswd = request.form.get('confirmpassword', '')
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
                user.add_user_to_session()
                return redirect(url_for('dashboard'))
        return render_template("register.html", errors=errors)

    @staticmethod
    def resetpassword():
        errors = []
        if request.method == 'POST':
            email = request.form.get('email', '')
            if not email:
                errors.append('Email cannot be empty.')
            else:
                user = User.query.filter_by(email=email).first()
                if user:
                    passwordreset = PasswordResets.query.filter_by(user_id=user.id).first()
                    if passwordreset:
                        db.session.delete(passwordreset)
                        db.session.commit()
                    passwordReset = PasswordResets(user.id, ''.join(
                        random.choice('0123456789qwertyuiopasdfghjklzxcvbnm') for i in range(16)),
                                                   DT.datetime.now() + DT.timedelta(hours=2))
                    db.session.add(passwordReset)
                    db.session.commit()
                    msg = Message("Password reset BlueGarden", sender='test9430384@gmail.com',
                                  recipients=[email])
                    msg.html = "<b>Click <a href = 'http://127.0.0.1:5000/resetpassword/%s/%s'>here</a> to reset your password</b>" % (
                    passwordReset.password_reset_token, passwordReset.user_id)
                    mail.send(msg)
                    return redirect(url_for('resetdone'))
                else:
                    errors.append('This email is not registered.')
        return render_template("resetpassword.html", errors=errors)

    @staticmethod
    def changepassword(token, user_id):
        errors = []
        if request.method == 'POST':
            user = User.query.get(user_id)
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            if password == confirm_password:
                user.set_password(password)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                errors.append('passwords did not match')
                return render_template("changepassword.html", errors=errors)
        passwordreset = PasswordResets.query.filter_by(user_id=user_id).first()
        if passwordreset:
            if passwordreset.password_reset_token == token and passwordreset.expire_time > DT.datetime.now():
                return render_template("changepassword.html")
            else:
                return 'token error'
        else:
            return ' no token'

    @staticmethod
    def resetdone():
        errors = []
        return render_template("resetdone.html", errors=errors)


    @staticmethod
    def logout():
        session.pop('logged_in', None)
        session.pop('id', None)
        session.pop('email', None)
        session.pop('firstname', None)
        session.pop('lastname', None)
        flash('You successfully logged out', 'success')
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
            flash('You success added crop')
        crop_m=Crop.query.all()
            
        return render_template("addcrop.html",crop_m=crop_m,errors = errors)

    @staticmethod
    def show_dashboard():
        id = session.get("id")
        recently_viewed = RecentProduce.query.order_by(RecentProduce.id.desc()).filter_by(user_id=id).limit(4)
        return render_template('dashboard.html', items=recently_viewed)


