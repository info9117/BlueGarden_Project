from shared import db


class Check(db.Model):
    __tablename__ = 'check'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(40), nullable=False)
    email = db.Column('email', db.String(40), nullable=False)
    phone = db.Column('phone', db.Integer)
    address = db.Column('address', db.String(40), nullable=False)
    discount = db.Column('discount', db.Integer)
    item_id = db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
    item = db.relationship('Item', foreign_keys=[item_id])
    total = db.Column('total', db.Float)

    def __init__(self, name, email, phone, address, item_id, discount, total):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.discount = discount
        self.item_id = item_id
        self.total = total
