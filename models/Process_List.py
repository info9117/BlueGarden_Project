from shared import db


class Process_List(db.Model):
    __tablename__ = 'Process_List'
    __table_args__ = (
    )
    id = db.Column('id', db.Integer, primary_key=True)
    process_name = db.Column('process_name', db.String(255))
    process_description = db.Column('process_description', db.String(255))

    def __init__(self, process_name, process_description):
        self.process_name = process_name
        self.process_description = process_description
