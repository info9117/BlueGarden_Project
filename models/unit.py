from shared import db


class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(10), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
