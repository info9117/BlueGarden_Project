from shared import db


class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column('id', db.Integer, primary_key=True)
    description = db.Column('description', db.String(255), nullable=False)
    farm_id = db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'), nullable=False)
    date = db.Column('date', db.Date, nullable=False)
    resource = db.Column('resource', db.String(255))#, db.ForeignKey('resource.id') nullable=False)

    def __init__(self, description, farm_id, date, resource):
        self.description = description
        self.farm_id = farm_id
        self.date = date
        self.resource = resource
