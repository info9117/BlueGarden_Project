

from shared import db


class Active_Process(db.Model):
    __tablename__ = 'active_process'
    
    id = db.Column('id', db.Integer, primary_key=True)
    Process_Template_ID = db.Column('Process_Template_ID', db.Integer), db.ForeignKey('Process_Template.Process_Template_ID'), nullable=False)
    user_id = db.Column('user_id', db.Integer), db.ForeignKey('user.id'), nullable=False)
    Start_Date = db.Column('Start_Date', db.Date, nullable=False)
    Progress = db.Column('progress', db.Integer), db.ForeignKey('active_activity.id'), nullable=True)
    Finish_Date = db.Column('Finish_Date', db.Date, nullable=True)
    Target_Type = db.Column('Target_Type', db.String(255), nullable=True)
    Target_ID = db.Column('Target_ID', db.Integer, nullable=True)
    

    def __init__(self, Process_Template_ID, user_id, Start_Date, Progress,Finish_Date,Target_Type,Target_ID):
        self.Process_Template_ID = Process_Template_ID
        self.user_id = user_id
        self.date = date
        self.Start_Date = Start_Date
        self.Progress = Progress#this is a foreign key to the last active_activity marked as completed
        self.Finish_Date = Finish_Date
        self.Target_Type = Target_Type
        self.Target_ID = Target_ID

