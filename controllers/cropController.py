from flask import request, render_template, redirect, url_for, flash, session

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
            oristate = Crop.query.get(crop_id)
            oristate.grow_state = new_state
            db.session.add(oristate)
            db.session.commit()
            flash("you successfully change the state")
            #return redirect(url_for('change_state',crop_id = crop_id))
            return redirect(url_for('addcrop'))
            
        return render_template('change_state.html',errors = errors,crop_id=crop_id)
        
    '''@staticmethod
    def add_active_process():
        erros=[]
        if request.method == 'POST':'''



    