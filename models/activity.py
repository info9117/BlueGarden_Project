from shared import db


class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column('id', db.Integer, primary_key=True)
    description = db.Column('description', db.String(255), nullable=False)
    date = db.Column('date', db.String(255), nullable=False)#db.Date
    resource = db.Column('resource', db.String(255))#, db.ForeignKey('resource.id'), nullable=False)
    field_id = db.Column('field_id', db.Integer)#, db.ForeignKey('field.id'), nullable=False)
    

    def __init__(self, description, field_id, date, resource):
        self.description = description
        self.field_id = field_id
        self.date = date
        self.resource = resource

