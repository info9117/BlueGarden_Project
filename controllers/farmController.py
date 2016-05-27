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
        user = User.query.get(User.query.filter_by(email=session['email']).first().id)
        works = Works.query.filter_by(user_id=user.id).all()
        farms = []
        [[farms.append(farm) for farm in db.session.query(Farm).filter_by(id=farm.farm_id).all()] for farm in works]
        return farms
        
    @staticmethod
    def get_farm_resources(farm_id):
        
        db.session.add(Resource('fertiliser',farm_id))#
        db.session.commit()
        resources = Resource.query.filter_by(farm_id=farm_id).all()
        return resources

    @staticmethod
    def get_resources():
        return db.session.query(Resource_List).order_by(Resource_List.id.asc()).all()

 
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
    def activity(process_id):
        #to create an activity not assigned to process: GET ../activity/0

        resources = []
        activities = []
        errors = []
        processes = []

        [processes.append(process) for process in FarmController.get_processes()]
        [activities.append(activity) for activity in FarmController.get_activities()]
        [resources.append(resource) for resource in FarmController.get_resources()]

        if request.method == 'POST':

            req_resource_id = request.form.get('resource', '')
            activity_description = request.form.get('description', '')
            process = request.form.get('process', '')
            activity = request.form.get('activity', '')
            if activity:
                db.session.add(Process_Steps(process, activity))
                db.session.commit()
                flash("Activity was recorded")
                process = Process_List.query.get(process)
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
        process=''
        if process_id:
            process = Process_List.query.get(process_id)
        return render_template('activity.html', process=process, resources=resources, errors=errors, processes=processes, activities=activities)
    
    @staticmethod
    def init_process(Active_Process_ID,Process_Template_ID):
        process_steps = Process_Steps.query.filter_by(procedure_id=Process_Template_ID).all()
        for step in process_steps:
            Action_Completed=False
            Activity_ID = step.activity_id
            db.session.add(Active_Activity(Active_Process_ID, Activity_ID, Action_Completed))
            db.session.commit()

    
    @staticmethod
    def active_process(process_or_crop,id):
        errors=[]
        processes=[]
        other=False
        fields=[]
        farms=[]
        crops = []

        target = request.form.get('target',"")
        farm = request.form.get('farm',False)
        field = request.form.get('field',False)
        crop = request.form.get('crop',False)
        Start_Date = request.form.get('date', False)
        user_id = FarmController.get_user().id
        process = request.form.get('process',False)
        other_target = request.form.get('other_target',False)

        if process_or_crop=="process":
            process = Process_List.query.get(id)
        elif process_or_crop=="crop":
            target="crop"
            crop=Crop.query.get(id)

        if target=='other':
            other=True
        elif target=='field':
            [fields.append(field) for field in FarmController.get_user_fields()]
        elif target=='farm':
            [farms.append(farm) for farm in FarmController.get_user_farms()]
        elif target=='crop':
            [crops.append(crop) for crop in FarmController.get_crops()]

        [processes.append(process) for process in FarmController.get_processes()]

        if request.method == 'POST':
            if not process or not Start_Date:
                print("error")
                errors.append("A process and start date must be selected")
            if target == '' and not errors:
                
                db.session.add(Active_Process(process.id, user_id, datetime.strptime(Start_Date, '%d %b, %Y'), None,None,None,None))
                db.session.commit()
                Active_Process_ID = db.session.query(Active_Process).order_by(Active_Process.id.desc()).first().id
                FarmController.init_process(Active_Process_ID, process.id)
                flash("New active process \""+Process_List.query.get(process.id).process_name+"\" commences on the "+Start_Date)
                return render_template('/active_process.html', processes=processes)

            if field or farm or crop or other_target and not errors:
                if field:
                    Target_Type = "field"
                    Target_ID = field
                if farm:
                    Target_Type = "farm"
                    Target_ID = farm
                if crop:
                    Target_Type = "crop"
                    Target_ID = crop
                    if process_or_crop=="crop":
                        Target_ID = crop.id
                if other_target:
                    Target_Type = "other"
                    Target_ID = other_target
                pydate = datetime.strptime(Start_Date, '%d %b, %Y')
                db.session.add(Active_Process(process.id, user_id, pydate, None,None,Target_Type,Target_ID))
                db.session.commit()
                Active_Process_ID = db.session.query(Active_Process).order_by(Active_Process.id.desc()).first().id
                FarmController.init_process(Active_Process_ID, process.id)
                flash("New active process \""+Process_List.query.get(process.id).process_name+"\" commences on the "+Start_Date+" for your "+Target_Type)
                return render_template('/active_process.html', processes=processes)
            #process = Process_List.query.get(process)
            return render_template('/active_process.html', errors=errors, processes=processes, date=Start_Date, process=process, target=target, other=other,  fields=fields,  farms=farms,  crops=crops)

        return render_template('/active_process.html',errors=errors, processes=processes, process=process, target=target, other=other, field=field, fields=fields, farm=farm, farms=farms, crop=crop, crops=crops)
         
