from flask import request, render_template, redirect, url_for, flash, session
from models import *

from datetime import datetime


class FarmController:

    @staticmethod
    def get_farm_fields(farm_id):
        
        #db.session.add(Field('east block', farm_id))#
        #db.session.commit()        
        fields = Field.query.filter_by(farm_id=farm_id).all()
        return fields
        
    @staticmethod
    def get_user_fields():
        fields = []
        farms = FarmController.get_user_farms
        for farm in farms:
            for field in FarmController.get_farm_fields(farm.id):
                fields.append(field)
        return fields
        
    
    @staticmethod
    def get_user():
        
        return User.query.get(User.query.filter_by(email=session['email']).first().id)

    @staticmethod
    def get_crops():
        db.session.add(Crop(9,"test crop","labile",1))
        db.session.add(Crop(8,"test crop","labile",2))
        db.session.commit()
        return db.session.query(Crop).order_by(Crop.crop_name).all()

    @staticmethod
    def get_user_farms():
        user = User.query.get(User.query.filter_by(email=session['email']).first().id)
        farms = Works.query.filter_by(user_id=user.id).all()
        return farms
        
    @staticmethod
    def get_farm_resources(farm_id):
        
        db.session.add(Resource('fertiliser',farm_id))#
        db.session.commit()
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
        resources = []
        activities = []
        errors = []
        processes = []
        #process = request.form.get('process', '')#
        for process in db.session.query(Process_List).order_by(Process_List.id.asc()).all():
                processes.append(process)
        for activity in db.session.query(Activity_List).order_by(Activity_List.id.asc()).all():
                activities.append(activity)
        #test
        db.session.add(Resource_List("fertilser"))
        db.session.add(Resource_List("weed killer"))
        ##
        db.session.commit()
        for resource in db.session.query(Resource_List).order_by(Resource_List.id.asc()).all():
                resources.append(resource)
        if request.method == 'POST':

            req_resource_id = request.form.get('resource', '')
            activity_description = request.form.get('description', '')
            process = request.form.get('process', '')
            activity = request.form.get('activity', '')
            if activity:
                db.session.add(Process_Steps(process, activity))
                db.session.commit()
                flash("Activity was recorded")
                return render_template('activity.html', resources=resources, errors=errors, processes=processes, process=process, activities=activities)
            if not resources:
                errors.append("add some resources first!")
            if not process:
                errors.append("select a process")
            if not activity_description:
                errors.append("add an activity description")
            if not errors:
                db.session.add(Activity_List(activity_description, req_resource_id))
                newactivity = db.session.query(Activity_List).order_by(Activity_List.id.desc()).first().id
                db.session.add(Process_Steps(process, newactivity))
                db.session.commit()
                flash("Activity was recorded")
                #return render_template('process.html', process=Process_List.query.get(process))
                process = Process_List.query.get(process)
        return render_template('activity.html', resources=resources, errors=errors, processes=processes, process=process, activities=activities)
    
    @staticmethod
    def init_process(Active_Process_ID,Process_Template_ID):
        process_steps = Process_Steps.query.filter_by(procedure_id=Process_Template_ID).all()
        for step in process_steps:
            Action_Completed=False
            Activity_ID = step.activity_id
            db.session.add(Active_Activity(Active_Process_ID, Activity_ID, Action_Completed))
            db.session.commit()
    
    @staticmethod
    def get_processes():
        return db.session.query(Process_List).order_by(Process_List.id.asc()).all()
    
    @staticmethod
    def active_process():
        processes=[]
        other=False
        fields=[]
        farms=[]
        crops = []
        for process in FarmController.get_processes():
            processes.append(process)
        target = request.form.get('target',"")
        farm = request.form.get('farm',False)
        field = request.form.get('field',False)
        crop = request.form.get('crop',False)
        Start_Date = request.form.get('date', '')
        user_id = FarmController.get_user().id
        process = request.form.get('process','')

        print("target is:"+target)
        if target=='other':
            other=True
            print("target other selected")
        elif target=='field':
            for field in FarmController.get_user_fields():
                fields.append(field)
        elif target=='farm':
            for farm in FarmController.get_user_farms():
                farms.append(farm)
        elif target=='crop':
            for crop in FarmController.get_crops():
                crops.append(crop)

        if request.method == 'POST':
            Process_Template_ID = request.form.get('process','')

            Start_Date = datetime.strptime(Start_Date, '%d %b, %Y')

            if target=='':
                
                db.session.add(Active_Process(Process_Template_ID, user_id, Start_Date, None,None,None,None))
                db.session.commit()
                Active_Process_ID = db.session.query(Active_Process).order_by(Active_Process.id.desc()).first().id
                FarmController.init_process(Active_Process_ID, Process_Template_ID)
                
                return render_template('/active_process.html', processes=processes)
            if field or farm or crop:
                if field:
                    Target_Type = "field"
                    Target_ID = field
                if farm:
                    Target_Type = "farm"
                    Target_ID = farm
                if crop:
                    Target_Type = "crop"
                    Target_ID = crop
                #db.session.add(Active_Process(int(Process_Template_ID), user_id, Start_Date, None,None,Target_Type,Target_ID))
                db.session.add(Active_Process(int(Process_Template_ID), user_id, Start_Date, None,None,Target_Type,1))
                db.session.commit()
                Active_Process_ID = db.session.query(Active_Process).order_by(Active_Process.id.desc()).first().id
                FarmController.init_process(Active_Process_ID, Process_Template_ID)
            return render_template('/active_process.html', processes=processes, process=process, target=target, other=other, field=field, fields=fields, farm=farm, farms=farms, crop=crop, crops=crops)

            


        #return render_template('/active_process.html', target=target, crops=crops,  fields=fields,farms=farms, process=process, other=other, processes=processes)
            
            
        return render_template('/active_process.html', processes=processes, process=process, target=target, other=other, field=field, fields=fields, farm=farm, farms=farms, crop=crop, crops=crops)
         
