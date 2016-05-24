from shared import db


class Price(db.Model):
    __tablename__ = 'prices'
    __table_args__ = (
        db.PrimaryKeyConstraint('produce_id', 'unit_id', name='OneFarmerOneFarmOneEntry_CK'),
    )
    produce_id = db.Column('produce_id', db.Integer, db.ForeignKey("produces.id"), nullable=False)
    unit_id = db.Column('unit_id',  db.Integer, db.ForeignKey("units.id"), nullable=False)
    unit = db.relationship("Unit", foreign_keys=[unit_id])
    price = db.Column('price', db.Float, nullable=False)

    def __init__(self, produce_id, unit_id, price):
        self.produce_id = produce_id;
        self.unit_id = unit_id
        self.price = price
