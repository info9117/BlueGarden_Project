from shared import db


class Produce(db.Model):
    __tablename__ = 'produces'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), nullable=False)
    # Vegetables, Fruits, Grains, meats, diary
    category = db.Column('category', db.String(40), nullable=False)
    description = db.Column('description', db.String(255))
    image_id = db.Column('image_id', db.Integer, db.ForeignKey("images.id"))

    def __init__(self, name, description,  category, image_id):
        self.name = name
        self.description = description
        self.category = category
        self.image_id = image_id
