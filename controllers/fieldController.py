from flask import request, render_template, redirect, url_for, flash, session
from models.user import *
from models.works import *
from models.farm import *
#from models.produce import *
from models.address import *
from models.field import *

class FieldController:

    @staticmethod
    def addField():
        myfields = []
        myfarms = []
        errors = []
        user = User.query.get(User.query.filter_by(email=session['email']).first().id)


        if user.type == 'C':  # Display users previously added farms
            for farm in Works.query.filter_by(user_id=user.id).all():
                #myfarms[farm] = db.session.query(Field.fielme).dNafilter(Field.farmName == farm).all()
                myfarms.append(Farm.query.get(farm.farm_id).name)
        else:
            errors.append("You dont have any farms yet. Please add a farm.")

        for farm in myfarms:
            for field in (Field.query.filter_by(farmName = farm)):
                fullfield = (field.fieldName + ' at ' + field.farmName)
                myfields.append(fullfield)
#                myfields.append(field.fieldName )
                #myfields.append(field)



        if request.method == 'POST':
            fieldname = request.form.get('fieldname', '')
            farmname = request.form.get('farmname', '')
            if farmname not in myfarms:
                errors.append("That's not your farm")
            if not fieldname:
                errors.append("You must enter a field name")
            if not farmname:
                errors.append("You must enter a farm name")

            if not errors:
                #add field:
                farm_id = Farm.query.filter_by(name=farmname).first().id

                field = Field(fieldname,farmname,farm_id)
                db.session.add(field)
                db.session.commit()
                return redirect(url_for('field'))
        return render_template("field.html", errors=errors, myfarms=myfarms, myfields = myfields)


