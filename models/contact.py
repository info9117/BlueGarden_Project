from shared import db
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

'''

This file will feature front end control through contact form webpage.
Validation rules will also be included in this file.
And through this file, there should be a link to backend feedback management portal/system.

'''

class Contact(db.Model):
    __tablename__ = 'feedback'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), nullable=False)
    email = db.Column('email', db.String(255), nullable=False)
    title = db.Column('title', db.String(255), nullable=False)
    enquiry = db.Column('enquiry',db.String(65535), nullable=False)

    def __init__(self, name, email, title, enquiry):
        self.name = name
        self.email = email
        self.title = title
        self.enquiry = enquiry




