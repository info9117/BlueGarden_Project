
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
