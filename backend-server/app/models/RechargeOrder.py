from . import db


class RechargeOrder(db.Model):
    __tablename__ = 'recharge_order'
    oid = db.Column('oid', db.TEXT, primary_key=True, unique=True, index=True, nullable=False)
    h5id = db.Column('h5id', db.TEXT, unique=True, nullable=False)
    payid = db.Column('payid', db.TEXT, nullable=False, default='-')
    uid = db.Column('uid', db.TEXT, nullable=False)
    payment = db.Column('payment', db.TEXT, nullable=False)
    status = db.Column('status', db.TEXT, default="wait", nullable=False)
    price = db.Column('price', db.FLOAT, nullable=False)
    ctime = db.Column('ctime', db.TEXT, nullable=False)
    ptime = db.Column('ptime', db.TEXT, nullable=True, default='-')
