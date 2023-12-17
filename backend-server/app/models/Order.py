from . import db


class Order(db.Model):
    __tablename__ = 'orders'
    oid = db.Column('oid', db.TEXT, primary_key=True, unique=True, index=True, nullable=False)
    uid = db.Column('uid', db.INTEGER, nullable=False)
    type = db.Column('type', db.TEXT, nullable=False)
    state = db.Column('state', db.TEXT, default="待付款", nullable=False)
    ctime = db.Column('ctime', db.TEXT, nullable=False)
    ptime = db.Column('ptime', db.TEXT, nullable=True, default='-')
    dtime = db.Column('dtime', db.TEXT, nullable=True, default='-')
    info = db.Column('info', db.JSON, nullable=False)
    price = db.Column('price', db.FLOAT, nullable=False)
    extra = db.Column('extra', db.TEXT, nullable=True)
