from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from shared import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(255), nullable=False)
    last_name = db.Column('last_name', db.String(255), nullable=False)
    email = db.Column('email', db.String(255), unique=True)
    password = db.Column('password', db.String(128), nullable=False)
    # Buyer - B, Buyer & Farmer - C
    type = db.Column('type', db.String(1), default='B')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return self.email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_user_farmer(self):
        self.type = 'C'

    def add_user_to_session(self):
        session['logged_in'] = True
        session['id'] = self.id
        session['email'] = self.email
        session['firstname'] = self.first_name
        session['lastname'] = self.last_name
        session['type'] = self.type
