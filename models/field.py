"""
from shared import db

class Field(db.Model):
    __tablename__ = 'field'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    farm_id = db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'),nullable=False)
    
    def __init__(self, name, farm_id):
        self.name = name
        self.farm_id = farm_id
    
"""
from shared import db
from sqlalchemy import PrimaryKeyConstraint


class Field(db.Model):
    __tablename__ = 'field'
    __table_args__ = (
    )

    id = db.Column('id', db.Integer, primary_key=True)
    fieldName = db.Column('fieldName', db.String(255), nullable=False)
    farmName = db.Column('farmName', db.String(255), db.ForeignKey('farms.name'), nullable=False)
    farm_id = db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'),nullable=False)
    
    def __init__(self, name, farmname, farm_id):
        self.fieldName = name
        self.farmName = farmname
        self.farm_id = farm_id


