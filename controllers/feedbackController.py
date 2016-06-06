from flask import request, render_template, session, redirect, url_for, flash

from models.feedback import *


class FeedbackController:
    @staticmethod
    def feedback():
        success = False
        errors=[]
        if request.method == 'POST':
            username = request.form.get('username', '')
            email = request.form.get('email', '')
            subject = request.form.get('subject', '')
            message = request.form.get('message', '')
            if not username:
                errors.append('Name cannot be empty')
            if not email:
                errors.append('Email Id cannot be empty')
            if not subject:
                errors.append('Title cannot be empty')
            if not message:
                errors.append('Tell me something more! >_<')
            if not errors:

                feedback = Feedback(username, email, subject, message)
                db.session.add(feedback)
                db.session.commit()

                success = True

        return render_template("feedback.html", success=success)
