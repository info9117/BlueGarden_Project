import os
from models import Produce, Image, Farm, Address, Grows, Price, Unit, Works
from shared import db
from flask import request, render_template, abort, session, redirect, flash, url_for
from werkzeug.utils import secure_filename
import utilities


class ProduceController:

    @staticmethod
    def add_produce(farm_id, upload_folder):
            errors = []
            if not Works.query.filter_by(user_id=session.get('id')).filter_by(farm_id=farm_id).first():
                flash("Sorry, This farm doesn't belong to you", 'error')
                return redirect(url_for('sell'))   
            if request.method == 'POST':
                name = request.form.get('name', '')
                description = request.form.get('description', '')
                category = request.form.get('category', '')
                selected_units = request.form.get('units', '')
                prices = {}
                for sel_unit in selected_units:
                    prices[sel_unit] = request.form.get('price' + selected_units)
                file = request.files['prod_image']
                if not name:
                    errors.append('Name cannot be empty')
                if not description:
                    errors.append('Description cannot be empty')
                if not category:
                    errors.append('Please choose a category for the produce')
                if not selected_units:
                    errors.append('Please choose the units you wish to sell in')
                if len(prices) < len(selected_units):
                    errors.append('Please enter the prices for the produce')
                if not file or not utilities.allowed_file(file.filename):
                    errors.append("Please upload 'png', 'jpg', 'jpeg' or 'gif' image for produce")
                if not errors:
                    directory = os.path.join(upload_folder, 'produce/' + str(farm_id) + '/')
                    os.makedirs(os.path.dirname(directory), exist_ok=True)
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(directory, filename))
                    img = Image('produce/' + str(farm_id) + '/' + filename)
                    db.session.add(img)
                    db.session.flush()
                    prod = Produce(name, description, category, img.id)
                    db.session.add(prod)
                    db.session.flush()
                    db.session.add(Grows(farm_id, prod.id))
                    for p in prices:
                        db.session.add(Price(prod.id, p, prices[p]))
                        db.session.flush()
                    db.session.commit()
                    return 'Success'
            units = Unit.query.all()
            current_farm = Farm.query.get(farm_id)
            if not current_farm:
                abort(404)
            farm_address = Address.query.get(current_farm.address_id)
            return render_template('add_produce.html', units=units, farm=current_farm, address=farm_address, errors=errors)
