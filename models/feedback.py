from shared import db


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255), nullable=False)
    email = db.Column('email', db.String(255), nullable=False)
    subject = db.Column('subject', db.String(255), nullable=False)
    message = db.Column('message', db.String(255), nullable=False)
    

    def __init__(self, username, email, subject, message):
        self.username = username
        self.email = email
        self.subject = subject
        self.message = message

