from flask import request, render_template, redirect, url_for, flash, session
from models.user import *
from models.works import *
from models.farm import *
#from models.produce import *
from models.address import *
from models.crop import *
from models.field import *
from models.activity import *
from models.resource import *
from datetime import datetime


class FarmController:

    @staticmethod
    def get_farm_fields(farm_id):
        if not farm_id:
            return redirect(url_for('activity'))
        #db.session.add(Field('east block', farm_id))#
        #db.session.commit()        
        fields = Field.query.filter_by(farm_id=farm_id).all()
        return fields
        

    @staticmethod
    def get_user_farms():
        user = User.query.get(User.query.filter_by(email=session['email']).first().id)
        farms = Works.query.filter_by(user_id=user.id).all()
        return farms
        
    @staticmethod
    def get_farm_resources(farm_id):
        if not farm_id:
            return redirect(url_for('activity'))
        #db.session.add(Resource('fertiliser',farm_id))#
        #db.session.commit()
        resources = Resource.query.filter_by(farm_id=farm_id).all()
        return resources
 
    @staticmethod
    def add_farm():
        errors = []
        myfarms = []
        names = []
        user = User.query.get(User.query.filter_by(email=session['email']).first().id)
        if user.type == 'C':
            for farm in FarmController.get_user_farms():
                myfarms.append(Farm.query.get(farm.farm_id))
                names.append(Farm.query.get(farm.farm_id).name)
        else:
            errors.append("You dont have any farms yet. Please add a farm.")

        if request.method == 'POST':
            name = request.form.get('name', '')
            if name in names:
                errors.append("Already Exists")
                return render_template("sell.html", errors=errors, myfarms=myfarms)
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
            else:

                #add farm address:
                address = Address(address1,address2,city,state,country,postcode)
                db.session.add(address)
                #add new farm:
                address_id = db.session.query(Address).order_by(Address.id.desc()).first().id
                farm = Farm(name,address_id)
                db.session.add(farm)
                #add farm worker and change user type flag:
                farm_id = db.session.query(Farm).order_by(Farm.id.desc()).first().id
                db.session.add(Works(user.id,farm_id))
                User.set_user_farmer(user)
                db.session.commit()
                return redirect(url_for('sell'))         
        return render_template("sell.html", errors=errors, myfarms=myfarms)  
        
    @staticmethod
    def activity():
        myfarms = []
        resources = []
        fields = []
        
        for farm in FarmController.get_user_farms():
            myfarms.append(Farm.query.get(farm.farm_id))
            
        farm_id = request.form.get('farm', '')
        resource = request.form.get('resource', '')
        field = request.form.get('field', '')
        description = request.form.get('description', '')
        date = request.form.get('date', '')
        if resource == '' and request.method == 'POST':
            selectedfarm = Farm.query.get(farm_id)
            for resource in FarmController.get_farm_resources(farm_id):
                resources.append(resource)
            for field in FarmController.get_farm_fields(farm_id):
                fields.append(field)
            return render_template('activity.html', selectedfarm=selectedfarm, 
                                                        myfarms=myfarms, resources=resources, fields=fields)
           
        if request.method == 'POST' and resource != '':
            if field =='' or date =='' or description =='':
                flash("You must fill out all the forms") 
                return render_template('activity.html', myfarms=myfarms, resources=resources, fields=fields)
            
            date_obj = datetime.strptime(date, '%d %b, %Y')#.date()
            if request.form.get('harvest', '') == 'on':
                sendto="add produce with args?"
                #crop = Crop.query.filter_by(farm_id=farm_id).first()
                #Crop.delete(crop)
                #add crop to produce??
            db.session.add(Activity(description,field,date,resource))
            db.session.commit()
            flash("Activity was recorded")       
        return render_template('activity.html', myfarms=myfarms)

