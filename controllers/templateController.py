from flask import request, render_template, redirect, url_for, flash, session
from models.user import *
from models.works import *
from models.farm import *
from models.address import *
from models.crop import *
from models.field import *
from models.activity import *
from models.resource import *
from datetime import datetime
from models.Process_List import *


class TemplateController:

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
                    errors.append("You must enter a Process name")
            if not process_description:
                    errors.append("You must enter a Process description")
            if not errors:
                    process = Process_List(process_name, process_description)
                    db.session.add(process)
                    db.session.commit()
                    return redirect(url_for('process'))
        return render_template("process.html", errors=errors, myProcesses=myProcesses)





