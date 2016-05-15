from shared import db
from sqlalchemy import PrimaryKeyConstraint


class Field(db.Model):
    __tablename__ = 'field'
    __table_args__ = (
    )

    id = db.Column('id', db.Integer, primary_key=True)
    fieldName = db.Column('fieldName', db.String(255), nullable=False)
    farmName = db.Column('farmName', db.String(255), nullable=False)

    def __init__(self, name, farmname):
        self.fieldName = name
        self.farmName = farmname


