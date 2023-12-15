from . import db, EntityBase


class User(db.Model, EntityBase):
    __tablename__ = 'users'
    uid = db.Column('uid', db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    mob = db.Column('mob', db.Integer, unique=True, nullable=False)
    pwd = db.Column('pwd', db.Text, nullable=False)
    balance = db.Column('balance', db.Float, nullable=False, default=1.0)
    wjx_set = db.Column('wjx_set', db.JSON, nullable=True)
