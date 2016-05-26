from flask import request, render_template, redirect, url_for, flash, session
from models import *

class ResourceController:
    @staticmethod
    def add_resource():
        errors = []
        if request.method =="POST":
            resource_id = request.form.get('resourceid', '')
            resource_description = request.form.get('resourcedescription','')
            Resource_List(resource_description, resource_id)
        render_template("addresource",errors)
