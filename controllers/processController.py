from flask import request, render_template, redirect, url_for, flash, session
from models import *
from datetime import datetime
from .farmController import FarmController as Farm

class ProcessController:

    # Open a new process template to record a set of farmer activities
    @staticmethod
    def add_process():
        errors = []
        myProcesses = []
        user = User.query.get(User.query.filter_by(email=session['email']).first().id)

        for process in Process_List.query.all():
            myProcesses.append(process)

        if request.method == 'POST':
            process_name = request.form.get('process_name', '')
            process_description = request.form.get('process_description', '')
            if not process_name:
                errors.append("Error - You must enter a Process name")
            if not process_description:
                errors.append("Error - You must enter a Process description")
            if not errors:
                process = Process_List(process_name, process_description)
                db.session.add(process)
                db.session.commit()
                return redirect(url_for('process'))
        return render_template("process.html", errors=errors, myProcesses=myProcesses)

    # Enter activity details used as steps in a farmer process
    @staticmethod
    def activity(process_id):
        # to create an activity not assigned to process: GET ../activity/0
        process = ''
        resources = []
        activities = []
        errors = []
        processes = []

        [processes.append(process) for process in Farm.get_processes()]
        [activities.append(activity) for activity in Farm.get_activities()]
        [resources.append(resource) for resource in Farm.get_resources()]

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
                return render_template('activity.html', resources=resources, errors=errors, processes=processes,
                                       process=process, activities=activities)
            if not resources:
                errors.append("add some resources first!")
            if not req_resource_id:
                errors.append("select a resource this time")
            if not process:
                errors.append("select a process")
            if not activity_description:
                errors.append("add an activity description")
            if not errors:
                db.session.add(Activity_List(activity_description, req_resource_id))
                newactivity = db.session.query(Activity_List).order_by(Activity_List.id.desc()).first().id
                db.session.add(Process_Steps(process, newactivity))
                db.session.commit()
                process = Process_List.query.get(process)
                flash("Activity \"" + activity_description + "\" was added to " + process.process_name)

        if process_id:
            process = Process_List.query.get(process_id)
        return render_template('activity.html', process=process, resources=resources, errors=errors, processes=processes,
                               activities=activities)

    # Using a process template, start an instance of a process to be tracked
    @staticmethod
    def active_process(process_or_crop, id):
        errors = []
        processes = []
        other = False
        fields = []
        farms = []
        crops = []

        target = request.form.get('target', "")
        farm = request.form.get('farm', False)
        field = request.form.get('field', False)
        crop = request.form.get('crop', False)
        Start_Date = request.form.get('date', False)
        user_id = Farm.get_user().id
        process = request.form.get('process', False)
        other_target = request.form.get('other_target', False)

        if process_or_crop == "process":
            process = Process_List.query.get(id)
        elif process_or_crop == "crop":
            target = "crop"
            crop = Crop.query.get(id)

        if target == 'other':
            other = True
        elif target == 'field':
            [fields.append(field) for field in Farm.get_user_fields()]
        elif target == 'farm':
            [farms.append(farm) for farm in Farm.get_user_farms()]
        elif target == 'crop':
            [crops.append(crop) for crop in Farm.get_crops()]

        [processes.append(process) for process in Farm.get_processes()]

        if request.method == 'POST':
            if not process or not Start_Date:
                errors.append("A process and start date must be selected")
            if target == '' and not errors:
                # A process commences with NULL target
                db.session.add(
                    Active_Process(process.id, user_id, datetime.strptime(Start_Date, '%d %B, %Y'), None, None, None, None))
                db.session.commit()
                Active_Process_ID = db.session.query(Active_Process).order_by(Active_Process.id.desc()).first().id
                ProcessController.init_process(Active_Process_ID, process.id)
                flash("New active process \"" + Process_List.query.get(
                    process.id).process_name + "\" commences on the " + Start_Date)
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
                    if process_or_crop == "crop":
                        Target_ID = crop.id
                if other_target:
                    Target_Type = "other"
                    Target_ID = other_target
                pydate = datetime.strptime(Start_Date, '%d %B, %Y')
                db.session.add(Active_Process(process.id, user_id, pydate, None, None, Target_Type, Target_ID))
                db.session.commit()
                Active_Process_ID = db.session.query(Active_Process).order_by(Active_Process.id.desc()).first().id
                ProcessController.init_process(Active_Process_ID, process.id)
                flash("New active process \"" + Process_List.query.get(process.id).process_name + "\" commences on the " +
                      Start_Date + " for your " + Target_Type)
                #..process started
                return render_template('/active_process.html', processes=processes)
            #..Request further specification of target (id/description)
            return render_template('/active_process.html', errors=errors, processes=processes, date=Start_Date,
                                   process=process,
                                   target=target, other=other, fields=fields, farms=farms, crops=crops)
        #..'GET'
        return render_template('/active_process.html', errors=errors, processes=processes, process=process,
                               target=target, other=other, field=field, fields=fields, farm=farm, farms=farms, crop=crop,
                               crops=crops)  # populate the process steps into the active activities table so they can have a progress and finish date

    # Add process template steps to set of active activities for tracking the progress through an active process
    @staticmethod
    def init_process(Active_Process_ID, Process_Template_ID):
        process_steps = Process_Steps.query.filter_by(procedure_id=Process_Template_ID).all()
        for step in process_steps:
            Action_Completed = False
            Activity_ID = step.activity_id
            db.session.add(Active_Activity(Active_Process_ID, Activity_ID, Action_Completed))
            db.session.commit()