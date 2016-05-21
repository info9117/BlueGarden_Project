

from shared import db


class Active_Activity(db.Model):
    __tablename__ = 'active_activity'
    
    id = db.Column('id', db.Integer, primary_key=True)
    Active_Process_ID = db.Column('Active_Process_ID', db.Integer), db.ForeignKey('Active_Process.id'), nullable=False)
    Activity_ID = db.Column('user_id', db.Integer), db.ForeignKey('Process_Steps.activity_id'), nullable=False)
    Action_Completed = db.Column('Start_Date', db.Boolean, nullable=False)

    

    def __init__(self, Active_Process_ID, user_id, Start_Date, Progress):
        self.Active_Process_ID = Active_Process_ID
        self.Activity_ID = Activity_ID
        self.Action_Completed = Action_Completed

        
