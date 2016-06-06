
from shared import db

class Crop(db.Model):
    __tablename__ = 'crop'
    id = db.Column('id', db.Integer, primary_key=True)
    crop_name = db.Column('crop_name', db.String(255))
    #if the crop is harvested, the value of state will be harvested. If not harvested yet, the value will be plant.
    grow_state = db.Column('grow_state', db.String(255))
    farm_id = db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'),nullable=False)
    active_process_id = db.Column('active_process_id', db.Integer, db.ForeignKey('Active_Process.id'),nullable=True)
    
    def __init__(self, id,  crop_name, grow_state, farm_id):
        self.id = id
        self.crop_name = crop_name
        self.grow_state = grow_state
        self.farm_id = farm_id


    '''def __init__(self, id, crop_name, grow_state, farm_id, active_process_id):
        self.id = id
        self.crop_name = crop_name
        self.grow_state = grow_state
        self.farm_id = farm_id
        self.active_process_id = active_process_id'''
    

