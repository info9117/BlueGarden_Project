from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


class Contact():
    # do we need to write contact form data into database?

    # which part should be programmed, including that "submit" button?

    #


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