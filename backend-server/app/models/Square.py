from . import db


class Square(db.Model):
    __tablename__ = 'square'
    aid = db.Column('aid', db.TEXT, primary_key=True)
    title = db.Column('title', db.TEXT, primary_key=False)
    short = db.Column('short', db.TEXT, nullable=False)
    stime = db.Column('stime', db.TEXT, nullable=False)
    atime = db.Column('atime', db.TEXT, nullable=True)
    location = db.Column('location', db.TEXT, nullable=True)
    limit = db.Column('limit', db.TEXT, nullable=True)
    score = db.Column('score', db.TEXT, nullable=True)
    raw = db.Column('raw', db.TEXT, nullable=True)
    link = db.Column('link', db.TEXT, nullable=True)
    n = db.Column('n', db.Integer, nullable=False, default=1)

