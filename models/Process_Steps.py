from shared import db

class Process_Steps(db.Model):
    __tablename__ = 'Process_Steps'
    __table_args__ = (
    )

    id = db.Column('id', db.Integer, primary_key=True)
    procedure_id = db.Column('procedure_id', db.String(255), db.ForeignKey('Process_List.id'), nullable=False)
    activity_id = db.Column('activity_id', db.String(255), db.ForeignKey('Activity_List.id'), nullable=False)

    def __init__(self, procedure_id, activity_id):
        self.procedure_id = procedure_id
        self.activity_id = activity_id

