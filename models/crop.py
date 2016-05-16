
from shared import db

class Crop(db.Model):
    __tablename__ = 'crop'
    id = db.Column('id', db.Integer, primary_key=True)
    crop_name = db.Column('crop_name', db.String(255))
    grow_state = db.Column('grow_state', db.String(255))
    farm_id = db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'),nullable=False)
    
    def __init__(self, id,  crop_name, grow_state, farm_id):
        self.id = id
        self.crop_name = crop_name
        self.grow_state = grow_state
        self.farm_id = farm_id
    