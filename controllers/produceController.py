import os
from models import Produce, Image, Farm, Address, Price, Unit, Works, Item
from shared import db
from flask import request, render_template, abort, session, redirect, flash, url_for
from flask_sqlalchemy import Pagination
from sqlalchemy import func, and_
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
                img = Image(filename, 'produce/' + str(farm_id) + '/' + filename)
                db.session.add(img)
                db.session.flush()
                prod = Produce(name, description, category, farm_id, img.id)
                db.session.add(prod)
                db.session.flush()
                for p in prices:
                    db.session.add(Price(prod.id, p, prices[p]))
                    db.session.flush()
                db.session.commit()
                return 'Success'
        units = Unit.query.all()
        current_farm = Farm.query.get(farm_id)
        if not current_farm:
            return abort(404)
        return render_template('add_produce.html', units=units, farm=current_farm, address=current_farm.address,
                               errors=errors)

    @staticmethod
    def browse_produce(page):
        results_per_page = 12
        results_filtered = False
        categories = ['Vegetable', 'Fruit', 'Grain', 'Meat', 'Diary', 'Other']
        category_filter = []
        for category in categories:
            if request.args.get(category.lower()) == 'on':
                category_filter.append(category.lower())
        location = request.args.get('location')
        if category_filter:
            results_filtered = True
            results = Produce.query.filter(func.lower(Produce.category).in_(category_filter)) \
                .order_by(Produce.id)
        if results_filtered and location:
                results = results.filter(Produce.farm_id == Farm.query.with_entities(Farm.id)
                                         .filter(and_(Farm.address_id == Address.id, func.lower(Address.city) ==
                                                      location.lower()))).order_by(Produce.id) \
                    .paginate(page, results_per_page, False)
        if not results_filtered and location:
            results_filtered = True
            results = Produce.query.filter(Produce.farm_id == Farm.query.with_entities(Farm.id)
                                           .filter(and_(Farm.address_id == Address.id, func.lower(Address.city) ==
                                                        location.lower()))).order_by(Produce.id) \
                .paginate(page, results_per_page, False)
        if results_filtered and not location:
            results = results.paginate(page, results_per_page, False)
            
        if not results_filtered:
            results = Produce.query.order_by(Produce.farm_id).paginate(page, results_per_page, False)
        total = results.total
        pagination = Pagination(results, page, results_per_page, total, results.items)
        return render_template('browse_produce.html', results=results.items, categories=categories,
                               pagination=pagination)

    @staticmethod
    def view_produce(produce_id):
        produce1 = Produce.query.get(produce_id)
        if request.method == 'POST':
            amount = request.form.get('amount')
            print('amount', type(amount))
            print('produce', type(produce1.prices[0].price))
            if amount:
                amount = request.form.get('amount', '')
                item1 = Item(produce1.prices[0].price, produce_id, amount)
                db.session.add(item1)
                db.session.commit()
                return render_template('view_produce.html', produce=produce1, total=item1.total)
            else:
                return render_template('view_produce.html', produce=produce1, total="wrong value")

        return render_template('view_produce.html', produce=produce1)