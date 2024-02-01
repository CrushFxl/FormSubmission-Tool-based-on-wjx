from . import db


class BusinessOrder(db.Model):
    __tablename__ = 'business_orders'
    oid = db.Column('oid', db.TEXT, primary_key=True, unique=True, index=True, nullable=False)
    uid = db.Column('uid', db.INTEGER, nullable=False)
    type = db.Column('type', db.TEXT, nullable=False)
    status = db.Column('status', db.INTEGER, default=0, nullable=False)
    ctime = db.Column('ctime', db.TEXT, nullable=False)
    ptime = db.Column('ptime', db.TEXT, nullable=True, default='-')
    dtime = db.Column('dtime', db.TEXT, nullable=True, default='-')
    config = db.Column('config', db.JSON, nullable=False)
    options = db.Column('options', db.JSON, nullable=False)
    price = db.Column('price', db.FLOAT, nullable=False)
    callback = db.Column('callback', db.INTEGER, nullable=False, default=1)
