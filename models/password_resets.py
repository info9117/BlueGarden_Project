from shared import db


class PasswordResets(db.Model):
    __tablename__ = 'password_resets'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    password_reset_token = db.Column('password_reset_token', db.String(128))
    expire_time = db.Column('expire_time', db.DateTime(128))

    def __init__(self, user_id, password_reset_token, expire_time):
        self.user_id = user_id
        self.password_reset_token = password_reset_token
        self.expire_time = expire_time

