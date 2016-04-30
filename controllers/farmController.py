from flask import request, render_template, redirect, url_for, flash, session
from models.user import *
from models.works import *
from models.farm import *
#from models.produce import *
from models.address import *

class FarmController:
 
    @staticmethod
    def farms_view():
        errors = []
        messages = []
        user = User.query.get(User.query.filter_by(email=session['email']).first().id)
        print(user.type)
        if user.type == 'C':
            usrid = user.id
            allfarmsiworkon = Works.query.filter_by(user_id=usrid).all()
            for farm in allfarmsiworkon:
                print(farm.farm_id)
                fid = farm.farm_id
                #print(Farm.query.get(farm.farm_id).name)
                errors.append(Farm.query.get(fid).name)
                
        #test exists a farm:
        #farm = Works.query.filter_by(user_id=user.id).first().farm_id
        #print(Farm.query.get(farm).name)
     #   else:
     #       errors.append("You dont have any farms yet. Please add a farm.")
   # @staticmethod
   # def add_farm():
        if request.method == 'POST':
            name = request.form.get('name', '')
            address1 = request.form.get('address1', '')
            address2 = request.form.get('address2', '')
            city = request.form.get('city', '')
            state = request.form.get('state', '')
            country = request.form.get('country', '')
            postcode = request.form.get('postcode', '')
            address = Address(address1,address2,city,state,country,postcode)
            db.session.add(address)
            db.session.commit()
            address_id = db.session.query(Address).order_by(Address.id.desc()).first().id
            farm = Farm(name,address_id)
            db.session.add(farm)
            db.session.commit()
            user = User.query.get(User.query.filter_by(email=session['email']).first().id)
            #user = User.query.filter_by(email=session['email']).first()
            farm_id = db.session.query(Farm).order_by(Farm.id.desc()).first().id
            db.session.add(Works(user.id,farm_id))#farm_id failing not null constraint??
            #db.session.add(Works(1,2))

            User.set_user_farmer(user)
            db.session.commit()
            print(user.type)
            return redirect(url_for('sell'))
        return render_template("sell.html", errors=errors)    
        

