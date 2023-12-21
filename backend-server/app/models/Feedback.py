from . import db


class Feedback(db.Model):
    __tablename__ = 'feedback'
    uid = db.Column(db.TEXT, primary_key=True)
    time = db.Column('time', db.TEXT, nullable=False)
    text = db.Column('text', db.TEXT, nullable=False)
    conn_info = db.Column('conn_info', db.TEXT, nullable=True)
