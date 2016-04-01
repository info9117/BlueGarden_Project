from werkzeug.security import generate_password_hash, check_password_hash
from main import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(255))
    last_name = db.Column('last_name', db.String(255))
    email = db.Column('email', db.String(255), unique=True)
    password = db.Column('password', db.String(128))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return '<Email ' + self.email + '>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)