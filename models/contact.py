from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


class Contact():
    '''

    This file will feature front end control through contact form webpage.
    Validation rules will also be included in this file.
    And through this file, there should be a link to backend feedback management portal/system.

    '''

    '''
    @staticmethod
    def contact():
        errors = []
        if request.method == 'POST':
            email = request.form.get('email', '')
            enquiry = request.form.get('enquiry', '')
            if not email:
                errors.append('Email cannot be empty')
            if not enquiry:
                errors.append('Tell us something! >_<')
            if not errors:
                flash('\nCongrats! You have sent us enquiry! We will reply to you shortly. ^_^')
                return redirect(url_for('contact_form'))
        return render_template("contact.html", errors=errors)

    '''