from shared import db


class Works(db.Model):
    __tablename__ = 'works'
    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'farm_id', name='OneFarmerOneFarmOneEntry_CK'),
    )

    user_id = db.Column('user_id', db.Integer, db.ForeignKey("users.id"), nullable=False)
    farm_id = db.Column('farm_id',  db.Integer, db.ForeignKey("farms.id"), nullable=False)

    def __init__(self, user_id, farm_id):
        self.id = user_id
        self.farm_id = farm_id
