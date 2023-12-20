from flask import Blueprint, request, session

from app.models import to_json
from app.routes.filters import login_required
from app.models.Order import Order
from app.models.User import User


query_bk = Blueprint('query', __name__, url_prefix='/query')


@query_bk.get('/order')
@login_required
def query_order():
    uid = session.get('uid')
    oid = request.args['oid']
    order = Order.query.filter(Order.oid == oid, Order.uid == uid).first()
    if order:
        return {"code": 1000, "order": to_json(order)}
    return {"code": 1001}


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
    pageObj = (Order.query.filter(Order.uid == uid,
                                  Order.state >= sRange[0],
                                  Order.state <= sRange[1])
               .order_by(Order.ctime.desc()).paginate(page=pn, per_page=10))
    ordersObj = pageObj.items
    orders = []
    for i in ordersObj:
        i = to_json(i)
        # 删除无用数据
        del i['info']['wjx_set']
        del i['uid']
        orders.append(i)
    max_pn = pageObj.pages
    return {"code": 1000, "orders": orders, "max_pn": max_pn}


@query_bk.post('/user')
@login_required
def query_user():
    uid = session.get('uid')
    user = User.query.filter(User.uid == uid).first()
    mob = str(user.mob)
    return {"code": 1000, "user": {"mob": mob[0:4]+'***'+mob[-4:],
                                   "balance": user.balance,
                                   "ing": user.ing,
                                   "done": user.done}}
