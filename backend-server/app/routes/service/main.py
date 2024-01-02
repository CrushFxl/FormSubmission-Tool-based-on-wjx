from flask import Blueprint, request
import time

from app.routes.filters import signature_verify
from app.models import db
from app.models.BusinessOrder import BusinessOrder as Order
from app.models.User import User

service_bk = Blueprint('service', __name__, url_prefix='/service')


@service_bk.post('/accept')
def accept():
    oid = request.form.get('oid')
    order = Order.query.filter(Order.oid == oid).first()
    order.status = 400
    db.session.commit()
    return {"code": 1000, "msg": "ok"}


@service_bk.post('/error')
def error():
    oid = request.form.get('oid')
    code = request.form.get('code')

    order = Order.query.filter(Order.oid == oid).first()
    order.status = int(code)

    user = User.query.filter(User.uid == order.uid).first()
    user.balance += order.price
    db.session.commit()
    return {"code": 1000, "msg": "ok"}


@service_bk.post('/complete')
def complete():
    oid = request.form.get('oid')
    order = Order.query.filter(Order.oid == oid).first()
    order.status = 500
    order.dtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # TODO: 还需要wjx_result
    db.session.commit()
    return {"code": 1000, "msg": "ok"}
