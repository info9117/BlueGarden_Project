from shared import db


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column('id', db.Integer, primary_key=True)
    price = db.Column('price', db.Float)
    unit_id = db.Column('unit_id', db.Integer, db.ForeignKey('units.id'))
    unit = db.relationship('Unit', foreign_keys=[unit_id])
    produce_id = db.Column('produce_id', db.Integer, db.ForeignKey('produces.id'))
    produce = db.relationship('Produce', foreign_keys=[produce_id])
    total = db.Column('total', db.Float)
    amount = db.Column('amount', db.Integer)

    def __init__(self, price, unit_id, produce_id, amount):
        self.price = price
        self.unit_id = unit_id
        self.produce_id = produce_id
        self.amount = amount
        self.calculate_total(self.price, self.amount)

    def calculate_total(self, price, amount):
        self.total = price * float(amount)
