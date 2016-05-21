from shared import db

class Activity_List(db.Model):
    __tablename__ = 'Activity_List'
    __table_args__ = (
    )

    id = db.Column('id', db.Integer, primary_key=True)
    activity_description = db.Column('activity_description', db.String(255), nullable=False)
    req_resource_id = db.Column('req_resource_id', db.Integer, db.ForeignKey('Resource_List.id'), nullable=False)

    def __init__(self, activity_description, req_resource_id):
        self.activity_description = activity_description
        self.req_resource_id = req_resource_id
