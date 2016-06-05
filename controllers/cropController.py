from flask import request, render_template, redirect, url_for, flash, session

from models import Active_Process, Active_Activity
from models.user import *
from models.crop import *
from models.address import *


class CropController:
    @staticmethod
    def change_state(crop_id):
        errors=[]
        
        if request.method == 'POST':
            new_state = request.form.get('change_state','')
            oristate = Crop.query.get(crop_id)
            oristate.grow_state = new_state
            db.session.add(oristate)
            db.session.commit()
            flash("you successfully change the state")
            #return redirect(url_for('change_state',crop_id = crop_id))
            return redirect(url_for('addcrop'))
            
        return render_template('change_state.html',errors = errors,crop_id=crop_id)

    @staticmethod
    def update_active_process(crop_id):
        errors = []
        #if request.method == 'POST':
            #update_crop_process = request.form.get('update_active_process','')
        act_process = Active_Process.query.filter_by(Target_ID = crop_id).first()
        act_activities = Active_Activity.query.filter_by(Active_Process_ID = act_process.id).all()

        if request.method=='POST':
            if request.form['submit'] =="finish_activity":
                activity_done_id = request.form.get('finish_activity','')
               # act_done_id = activity_done_id
                print(activity_done_id)
                activity_done = Active_Activity.query.filter_by(id = activity_done_id).first()

                activity_done.Action_Completed = True
                db.session.add(activity_done)
                db.session.commit()
                flash("you successfully finish this acitivity")
                return redirect(url_for('update_active_process', crop_id = crop_id))
            if request.form['submit'] == "finish_process":
                done = True
                process_done_id = request.form.get('finish_process','')
                process_done = Active_Process.query.filter_by(id = process_done_id).first()
                activity_done = Active_Activity.query.filter_by(Active_Process_ID = process_done_id).all()
                for act in activity_done:
                    if act.Action_Completed ==False:
                        done = False
                if done:
                    process_done.Finish_Date = True
                db.session.delete(process_done)
                db.session.commit()
                flash("you finished this process")
                return redirect(url_for("addcrop"))

        return render_template('update_active_process.html',errors = errors, crop_id = crop_id, act_activities  = act_activities )








        



    