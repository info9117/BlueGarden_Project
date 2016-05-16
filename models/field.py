
from shared import db

class Field(db.Model):
    __tablename__ = 'field'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    farm_id = db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'),nullable=False)
    
    def __init__(self, name, farm_id):
        self.name = name
        self.farm_id = farm_id
    
