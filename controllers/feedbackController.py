import sqlite3
from flask import request, render_template, session, redirect, url_for, flash, g

from models.feedback import *
from shared import db

DATABASE = '/bluegarden.db'


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

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db

    def query_db(query, args=(), one=False):
        cur = query.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    def view_feedback(self):
        user = Feedback.query.filter_by(username=username).first_or_404()
        return render_template('show_user.html', user=user)