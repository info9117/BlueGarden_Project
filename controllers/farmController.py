from flask import request, render_template, redirect, url_for, flash, session
from models import *


class FarmController:

    @staticmethod
    def get_farm_fields(farm_id):
        fields = Field.query.filter_by(farm_id=farm_id).all()
        return fields
        
    @staticmethod
    def get_user_fields():
        fields = []
        farms = FarmController.get_user_farms()
        for farm in farms:
            for field in FarmController.get_farm_fields(farm.id):
                fields.append(field)
        return fields

    @staticmethod
    def get_processes():
        return db.session.query(Process_List).order_by(Process_List.id.asc()).all()

    @staticmethod
    def get_activities():
        return db.session.query(Activity_List).order_by(Activity_List.id.asc()).all()
    
    @staticmethod
    def get_user():
        return User.query.get(User.query.filter_by(email=session['email']).first().id)

    @staticmethod
    def get_crops():
        return db.session.query(Crop).order_by(Crop.crop_name).all()

    @staticmethod
    def get_user_farms():
        user = FarmController.get_user()
        works = Works.query.filter_by(user_id=user.id).all()
        farms = []
        [[farms.append(farm) for farm in db.session.query(Farm).filter_by(id=farm.farm_id).all()] for farm in works]
        return farms

    @staticmethod
    def get_resources():
        return db.session.query(Resource_List).order_by(Resource_List.id.asc()).all()

    # User adds a farm they work on. Naive:Does not check for existing farms added by other users!
    @staticmethod
    def add_farm():
        errors = []
        myfarms = []
        names = []
        user = User.query.get(User.query.filter_by(email=session['email']).first().id)
        if user.type == 'C':
            for farm in FarmController.get_user_farms():
                myfarms.append(farm)
                names.append(farm.name)
        else:
            errors.append("You dont have any farms yet. Please add a farm.")

        if request.method == 'POST':
            name = request.form.get('name', '')
            if name in names:
                errors.append("Already Exists")
                return render_template("farm.html", errors=errors, myfarms=myfarms)
            address1 = request.form.get('address1', '')
            address2 = request.form.get('address2', '')
            city = request.form.get('city', '')
            state = request.form.get('state', '')
            country = request.form.get('country', '')
            postcode = request.form.get('postcode', '')
            if not name:
                errors.append("You must enter a name")
            if not address1:
                errors.append("You must enter an address")
            elif not errors:

                #add farm address:
                address = Address(address1,address2,city,state,country,postcode)
                db.session.add(address)
                #add new farm:
                address_id = db.session.query(Address).order_by(Address.id.desc()).first().id
                farm = Farm(name,address_id)
                db.session.add(farm)
                #add farm worker and change user type flag to farmer:
                farm_id = db.session.query(Farm).order_by(Farm.id.desc()).first().id
                db.session.add(Works(user.id,farm_id))
                User.set_user_farmer(user)
                db.session.commit()

                return redirect(url_for('farm'))
        return render_template("farm.html", errors=errors, myfarms=myfarms)

