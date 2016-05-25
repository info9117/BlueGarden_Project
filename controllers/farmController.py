from flask import request, render_template, redirect, url_for, flash, session
from models import *

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
        resources = []
        errors = []
        processes = []
        for process in db.session.query(Process_List).order_by(Process_List.id.asc()).all():
                processes.append(process)
        for resource in db.session.query(Resource_List).order_by(Resource_List.id.asc()).all():
                resources.append(resource)
        if request.method == 'POST':
            db.session.add(Process_Steps(process, newactivity))
            db.session.commit()
            req_resource_id = request.form.get('resource', '')
            activity_description = request.form.get('description', '')
            process = request.form.get('process', '')
            activity = request.form.get('activity', '')
            if activity:
                db.session.add(Process_Steps(process, activity))
                db.session.commit()
                flash("Activity was recorded")
                return render_template('activity.html', resources=resources, errors=errors, processes=processes, process=process)
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
        return render_template('activity.html', resources=resources, errors=errors, processes=processes, process=process)
    
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
        for process in FarmController.get_processes():
            processes.append(process)

        if request.method == 'POST':
            Process_Template_ID = request.form.get('process','')
            target = request.form.get('target','')
            farm = request.form.get('farm',False)
            field = request.form.get('field',False)
            Start_Date = request.form.get('date', '')
            Start_Date = datetime.strptime(Start_Date, '%d %b, %Y')
            user_id = FarmController.get_user().id
            if not target:
                
                db.session.add(Active_Process(Process_Template_ID, user_id, Start_Date, null,null,null,null))
                db.commit()
                Active_Process_ID = db.session.query(Active_Process).order_by(Active_Process.id.desc()).first().id
                FarmController.init_process(Active_Process_ID, Process_Template_ID)
                
                return render_template('/active_process.html', processes=processes)
            if field or farm:
                if field:
                    Target_Type = "field"
                    Target_ID = field
                if farm:
                    Target_Type = "farm"
                    Target_ID = farm
                db.session.add(Active_Process(Process_Template_ID, user_id, Start_Date, null,null,Target_Type,Target_ID))
                db.commit()
                Active_Process_ID = db.session.query(Active_Process).order_by(Active_Process.id.desc()).first().id
                FarmController.init_process(Active_Process_ID, Process_Template_ID)
            return render_template('/active_process.html', processes=processes)
            
            other=False
            fields=[]
            farms=[]
            if target=='other':
                other=True
            elif target=='field':
                for field in FarmController.get_user_fields():
                    fields.append(field)
            elif target=='farm':
                for farm in FarmController.get_user_farms():
                    farms.append(farm)
            return render_template('/active_process.html', target=target, fields=fields,farms=farms, process=process, other=other)

    @staticmethod
    def linkToActivity(id):
        resources = []
        errors = []
        processes = []
        process = Process_List.query.filter_by(id=id).first()
        for resource in db.session.query(Resource_List).order_by(Resource_List.id.asc()).all():
                resources.append(resource)
        if request.method == 'POST':
            db.session.add(Process_Steps(process, newactivity))
            db.session.commit()
            req_resource_id = request.form.get('resource', '')
            activity_description = request.form.get('description', '')
            process = request.form.get('process', '')
            activity = request.form.get('activity', '')
            if activity:
                db.session.add(Process_Steps(process, activity))
                db.session.commit()
                flash("Activity was recorded")
                return render_template('activity.html', resources=resources, errors=errors, processes=processes, process=process)
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
            return render_template('activity.html', resources=resources, errors=errors, processes=processes, process=process)
        return render_template('activity.html', resources=resources, errors=errors, processes=processes, process=process)

