from . import db


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column('uid', db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    nick = db.Column('nick', db.Text, nullable=True, default='无名小卒')
    status = db.Column('status', db.Text, nullable=False, default='user')
    invite = db.Column('invite', db.Text, nullable=True)
    mob = db.Column('mob', db.Integer, unique=True, nullable=False)
    pwd = db.Column('pwd', db.Text, nullable=False)
    balance = db.Column('balance', db.Float, nullable=False, default=1.0)
    ing = db.Column('ing_ods', db.JSON, nullable=False, default=0)
    done = db.Column('done_ods', db.JSON, nullable=False, default=0)
