from shared import db

class Resource_List(db.Model):
    __tablename__ = 'Resource_List'
    __table_args__ = (
    )

    id = db.Column('id', db.Integer, primary_key=True)
    resource_description = db.Column('resource_description', db.String(255), nullable=False)

    def __init__(self, resource_description):
        self.resource_description = resource_description

