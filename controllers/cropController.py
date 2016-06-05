from flask import request, render_template, redirect, url_for, flash, session

from models import Active_Process, Active_Activity
from models.user import *
from models.crop import *
from models.address import *


class CropController:
    @staticmethod
    def addcrop():
        errors = []
        crop_m = []
        myfarm = []
        # user = User.query.get(User.query.filter_by(email=session['email']).first().id())
        # myfarms
        if request.method == 'POST':
            # if request.form['action']=="add crop":
            id = request.form.get('id', '')
            crop_name = request.form.get('cropname', '')
            grow_state = request.form.get('growstate', '')
            farm_id = request.form.get('farmid', '')
            crop = Crop(id, crop_name, grow_state, farm_id)
            db.session.add(crop)
            db.session.commit()
            flash('You success added crop')
        crop_m = Crop.query.all()
        return render_template("addcrop.html", crop_m=crop_m, errors=errors)

    @staticmethod
    def change_state(crop_id):
        errors=[]
        
        if request.method == 'POST':
            new_state = request.form.get('change_state','')
            #oristate = Crop.query.get(crop_id)
            oristate = Crop.query.filter_by(id = crop_id).first()
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
        act_process = Active_Process.query.filter_by(Target_ID = crop_id).first()
        act_activities = Active_Activity.query.filter_by(Active_Process_ID = act_process.id).all()

        if request.method=='POST':
            if request.form['submit'] =="finish_activity":
                activity_done_id = request.form.get('finish_activity','')
               # act_done_id = activity_done_id
                print(activity_done_id)
                activity_done = Active_Activity.query.filter_by(id = activity_done_id).first()
                print(activity_done)
                print(activity_done.Action_Completed)
                activity_done.Action_Completed = True
                db.session.add(activity_done)
                db.session.commit()
                print(activity_done.Action_Completed)

                act_process = Active_Process.query.filter_by(Target_ID = crop_id).first()
                act_activities = Active_Activity.query.filter_by(Active_Process_ID = act_process.id).all()
                flash("you successfully finish this acitivity")
                #return redirect(url_for('update_active_process', crop_id = crop_id, act_activities  = act_activities))
                return render_template('update_active_process.html',errors = errors, crop_id = crop_id, act_activities  = act_activities )

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
