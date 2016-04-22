from werkzeug.security import generate_password_hash, check_password_hash
from shared import db


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
        return self.email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Farm(db.Model):
    __tablename__ = 'farms'
    id = db.Column('id', db.Integer, primary_key=True)
    farm_name = db.Column('farm_name', db.String(50))
    address = db.Column('address', db.String(80), nullable=False)

    def __init__(self, id, farm_name, address):
        self.id = id
        self.farm_name = farm_name
        self.address = address

        
class Farmer(db.Model):
    __tablename__ = 'farmers'
    __table_args__ = (
        db.PrimaryKeyConstraint('id', 'farms', name='OneFarmerOneFarmOneEntry_CK'),
    )

    id = db.Column('id', db.Integer, db.ForeignKey("users.id"), nullable=False)
    farms = db.Column('farms',  db.Integer, db.ForeignKey("farms.id"), nullable=False)
    
    def __init__(self, id, farms):
        self.id = id
        self.farms = farms
        
        

