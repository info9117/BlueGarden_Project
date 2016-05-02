from shared import db


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column('id', db.Integer, primary_key=True)
    address1 = db.Column('address1', db.String(255), nullable=False)
    address2 = db.Column('address2', db.String(255))
    city = db.Column('city', db.String(255), nullable=False)
    state = db.Column('state', db.String(25), nullable=False)
    country = db.Column('country', db.String(4), nullable=False)
    post_code = db.Column('post_code', db.Integer, nullable=False)

    def __init__(self, address1, address2, city, state, country, post_code):
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.country = country
        self.post_code = post_code
