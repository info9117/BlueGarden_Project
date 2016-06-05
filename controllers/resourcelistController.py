from flask import request, render_template, redirect, url_for, flash, session
from models import *

class ResourceController:
    @staticmethod
    def add_resource():
        errors = []
        resourcefull=[]

        for resource in (Resource_List.query.all()):
            resourcefull.append(resource.resource_description)

        if request.method =="POST":
            #resource_id = request.form.get('resourceid', '')
            resource_description = request.form.get('resourcedescription','')
            resource_list = Resource_List(resource_description)
            db.session.add(resource_list)
            db.session.commit()
            flash('added resource successfully')
            return redirect(url_for('resource'))
        return render_template("resourcelist.html", errors = errors, resourcefull = resourcefull)
