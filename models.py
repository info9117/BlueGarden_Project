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
        
class Crop(db.Model):
    __tablename__ = 'crops'
    id = db.Column('id', db.Integer, primary_key=True)
    crop_name = db.Column('crop_name', db.String(255))
    grow_state = db.Column('grow_state', db.String(255))
    farm_id = db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'))
    
    def __init__(self, crop_name, grow_state, farm_id):
        #self.id = id
        self.crop_name = crop_name
        self.grow_state = grow_state
        self.farm_id = farm_id
    
    
    
    
    
class Farm(db.Model):
    __tablename__ = 'farms'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), nullable=False)
    #address_id = db.Column('address_id', db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    #produce_id = db.Column('produce_id', db.Integer, db.ForeignKey('produces.id'))

    '''def __init__(self, name, address_id, produce_id):
        self.name = name
        self.address_id = address_id
        self.produce_id = produce_id'''
        
    def __init__(self, name):
        self.name = name
        
        
        
        
'''class Addresses(db.Model):
    __tablename__ = 'addresses'
    id = db.Column('id', db.Integer, primary_key=True)
    address1 = db.Column('address1', db.String(255), nullable=False)
    address2 = db.Column('address2', db.String(255))
    city = db.Column('city', db.String(255), nullable=False)
    state = db.Column('state', db.String(25), nullable=False)
    country = db.Column('address1', db.String(2), nullable=False)
    post_code = db.Column('address1', db.Integer(10), nullable=False)

    def __init__(self, address1, address2, city, state, country, post_code):
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.country = country
        self.post_code = post_code'''