import json
from datetime import datetime

import requests
from flask import Blueprint, request, session
from app.routes.filters import login_required
from app.models.User import User
from app.models.Message import Message
from app.models.BusinessOrder import BusinessOrder as Order
from app.models import db

admin_bk = Blueprint('admin', __name__, url_prefix='/admin')


# 发送站内消息
@admin_bk.post('/send_msg')
@login_required
def send_msg():
    uid = session.get('uid')
    if uid != 123456:
        return {"code": 3000, "msg": "拒绝访问"}
    uid = request.form.get('uid')
    title = request.form.get('title')
    content = request.form.get('content')
    date = "回复于" + datetime.now().strftime('%Y-%m-%d %H:%M')
    mid = str(datetime.now().timestamp() * 1000)
    nick = User.query.filter(User.uid == uid).first().nick
    print("已发送，", uid, title, content, date, mid, nick)
    message = Message(mid=mid, uid=uid, nick=nick, title=title, content=content, date=date)
    db.session.add(message)
    db.session.commit()
    return {"code": 1000, "nick": nick}


# 查询订单备注
@admin_bk.post('/query_order')
@login_required
def query_order():
    uid = session.get('uid')
    if uid != 123456:
        return {"code": 3000, "msg": "拒绝访问"}
    oid = request.form.get('oid')
    order = Order.query.filter(Order.oid == oid).first()
    nick = User.query.filter(User.uid == order.uid).first().nick
    uid = order.uid
    remark = order.config
    return {"code": 1000, "nick": nick, "uid": uid, "remark": remark}


# 修改备注
@admin_bk.post('/modify_order')
@login_required
def modify_order():
    uid = session.get('uid')
    if uid != 123456:
        return {"code": 3000, "msg": "拒绝访问"}
    oid = request.form.get('oid')
    new_remark = request.form.get('remark')
    order = Order.query.filter(Order.oid == oid).first()
    order.config = json.loads(new_remark)
    db.session.commit()

    server = order.callback

    # 发送Post
    requests.post(url=server + '/modify_remark',
                  data={'oid': oid,
                        'remark': json.dumps(new_remark)})
    return {"code": 1000, "msg": "ok"}
