from . import db


class Message(db.Model):
    __tablename__ = 'message'
    mid =db.Column('mid', db.Text, nullable=False, primary_key=True)
    uid = db.Column('uid', db.Integer, nullable=False)
    nick = db.Column('nick', db.Text, nullable=True, default='无名小卒')
    status = db.Column('status', db.Integer, nullable=False, default=0)
    title = db.Column('title', db.Text, nullable=False, default='无标题')
    content = db.Column('content', db.Text, nullable=False, default='无内容')
    date = db.Column('date', db.Text, nullable=False, default='-')
