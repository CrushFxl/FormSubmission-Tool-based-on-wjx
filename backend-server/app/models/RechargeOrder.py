from . import db


class RechargeOrder(db.Model):
    __tablename__ = 'recharge_order'
    # 自己平台生成的订单号
    oid = db.Column('oid', db.TEXT, primary_key=True, unique=True, index=True, nullable=False)
    # 第三方H5支付平台订单号
    h5id = db.Column('h5id', db.TEXT, unique=True, nullable=False, default='-')
    # 微信支付宝官方订单号
    payid = db.Column('payid', db.TEXT, unique=True, nullable=False, default='-')
    uid = db.Column('uid', db.TEXT, nullable=False)
    payment = db.Column('payment', db.TEXT, nullable=False)
    status = db.Column('status', db.TEXT, default="wait", nullable=False)
    price = db.Column('price', db.FLOAT, nullable=False)
    ctime = db.Column('ctime', db.TEXT, nullable=False)
    ptime = db.Column('ptime', db.TEXT, nullable=True, default='-')
    sign = db.Column('sign', db.TEXT, nullable=False)
