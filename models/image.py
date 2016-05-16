from shared import db


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column('id', db.Integer, primary_key=True)
    filename = db.Column('filename', db.String(255), nullable=False)
    url = db.Column('url', db.String(255), nullable=False)

    def __init__(self, filename, url):
        self.filename = filename
        self.url = url
