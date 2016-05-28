from shared import db


class RecentProduce(db.Model):
    __tablename__ = 'recent_produce'
    id = db.Column('id', db.Integer, primary_key=True)
    produce_id = db.Column('produce_id',db.Integer, db.ForeignKey('produces.id'))
    produce = db.relationship("Produce", foreign_keys=[produce_id])
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys=[user_id])


    # Vegetables, Fruits, Grains, meats, diary


    def __init__(self, produce_id,user_id):
        self.produce_id = produce_id
        self.user_id = user_id
