from flask import request, render_template, redirect, url_for, flash, session

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
        if request.method == 'POST':
            update_crop_process = request.form.get('update_active_process','')
        return render_template('change_state.html',errors = errors, crop_id = crop_id)







        
    '''@staticmethod
    def add_active_process():
        erros=[]
        if request.method == 'POST':'''



    