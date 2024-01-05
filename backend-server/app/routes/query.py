from flask import Blueprint, request, session

from app.models import to_json
from app.routes.filters import login_required
from app.models.BusinessOrder import BusinessOrder as bOrder
from app.models.RechargeOrder import RechargeOrder as rOrder
from app.models.User import User


query_bk = Blueprint('query', __name__, url_prefix='/query')


# 查询业务订单
@query_bk.get('/order')
@login_required
def query_order():
    uid = session.get('uid')
    oid = request.args['oid']
    order = bOrder.query.filter(bOrder.oid == oid, bOrder.uid == uid).first()
    if order:
        return {"code": 1000, "order": to_json(order)}
    return {"code": 1001}


# 查询业务订单列表
@query_bk.post('/orders')
@login_required
def query_orders():
    uid = session.get('uid')
    type = request.args['type']
    pn = int(request.args['pn'])
    sRange = [100, 999]
    if type == 'all':
        sRange = [100, 999]
    elif type == 'ing':
        sRange = [400, 499]
    elif type == 'done':
        sRange = [500, 599]
    pageObj = (bOrder.query.filter(bOrder.uid == uid,
                                   bOrder.status >= sRange[0],
                                   bOrder.status <= sRange[1])
               .order_by(bOrder.ctime.desc()).paginate(page=pn, per_page=10))
    ordersObj = pageObj.items
    orders = []
    for i in ordersObj:
        i = to_json(i)
        orders.append(i)
    # max_pn = pageObj.pages
    return {"code": 1000, "orders": orders}


# 查询用户主页信息
@query_bk.post('/user')
@login_required
def query_user():
    uid = session.get('uid')
    user = User.query.filter(User.uid == uid).first()
    return {"code": 1000, "user": {"nick": user.nick,
                                   "balance": user.balance,
                                   "ing": user.ing,
                                   "done": user.done}}


# 查询充值订单支付状态
@query_bk.post('/recharge')
@login_required
def query_recharge_order():
    uid = session.get('uid')
    oid = request.form.get('oid')
    recharge_order = rOrder.query.filter(rOrder.oid == oid).first()
    if recharge_order.uid != str(uid):
        return {"code": 2000, "msg": '拒绝访问'}
    return {"code": 1000, "msg": 'ok', 'status': recharge_order.status}
