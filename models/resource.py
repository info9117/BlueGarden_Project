
from shared import db

class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    #quantity = db.Column('quantity', db.String(255))
    farm_id = db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'),nullable=False)
    
    def __init__(self, name, farm_id):
        self.name = name
        #self.quantity = quantity
        self.farm_id = farm_id
    
