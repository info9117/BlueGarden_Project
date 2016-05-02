from shared import db


class Farm(db.Model):
    __tablename__ = 'farms'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), nullable=False)
    address_id = db.Column('address_id', db.Integer, db.ForeignKey('addresses.id'), nullable=False)

    def __init__(self, name, address_id):
        self.name = name
        self.address_id = address_id