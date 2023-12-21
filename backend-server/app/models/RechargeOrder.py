from . import db


class RechargeOrder(db.Model):
    __tablename__ = 'recharge_order'
    roid = db.Column('roid', db.TEXT, primary_key=True, unique=True, index=True, nullable=False)
    uid = db.Column('oid', db.TEXT, nullable=False)
    payment = db.Column('payment', db.TEXT, nullable=False)
    state = db.Column('state', db.INTEGER, default=100, nullable=False)
    price = db.Column('price', db.FLOAT, nullable=False)
    ctime = db.Column('ctime', db.TEXT, nullable=False)
    ptime = db.Column('ptime', db.TEXT, nullable=True, default='-')
