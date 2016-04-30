from shared import db


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column('id', db.Integer, primary_key=True)
    url = db.Column('url', db.String(255), nullable=False)

    def __init__(self, filename):
        self.url = filename
