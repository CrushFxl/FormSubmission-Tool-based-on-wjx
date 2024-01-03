from flask import Blueprint, request

from app.routes.filters import signature_verify
from app.models import db
from app.models.BusinessOrder import BusinessOrder as Order
from app.models.User import User

task_bk = Blueprint('api', __name__)


@task_bk.post('/update')
def update():
    oid = request.form.get('oid')
    status = int(request.form.get('status'))
    order = Order.query.filter(Order.oid == oid).first()
    user = User.query.filter(User.uid == order.uid).first()

    # 更新订单状态
    order.status = status
    if 400 <= status <= 499:
        user.ing += 1
    elif 500 <= status <= 599:
        user.ing -= 1
        user.done += 1
    elif status >= 900:
        user.ing -= 1
        user.balance += order.price     # 退款

    db.session.commit()
    return {"code": 1000, "msg": "ok"}
