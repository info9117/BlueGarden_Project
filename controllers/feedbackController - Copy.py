<<<<<<< HEAD
from flask import request, render_template, redirect, url_for, flash, session

from models.contact import Contact
from models.farm import *


class FeedbackController:
    @staticmethod
    def feedback():
        errors = []
        if request.method == 'POST':
            name = request.form.get('name', '')
            email = request.form.get('email', '')
            title = request.form.get('title', '')
            enquiry = request.form.get('enquiry', '')
            if not name:
                errors.append('Name cannot be empty')
            if not email:
                errors.append('Email Id cannot be empty')
            if not title:
                errors.append('Title cannot be empty')
            if not enquiry:
                errors.append('Tell me something more! >_<')
            if not errors:
                feedback = Contact(name, email, title, enquiry)
                db.session.add(feedback)
                db.session.commit()
                flash('Your feedback is sent. We will contact you shortly. ^_^')
                return redirect(url_for('contact'))
        return render_template("contact.html", errors=errors)

=======
from flask import request, render_template, session, redirect, url_for, flash

from models.feedback import *

class FeedbackController:
	@staticmethod
	def feedback():
		success = False

		if request.method == 'POST':
			username = request.form.get('username', '')
			email = request.form.get('email', '')
			subject = request.form.get('subject', '')
			message = request.form.get('message', '')

			feedback = Feedback(username, email, subject, message)
			db.session.add(feedback)
			db.session.commit()

			success = True

		return render_template("feedback.html", success=success)




>>>>>>> origin/sprint-3-himika-test-pass
