import json
import os

import requests
from flask import Blueprint, request

from app.models import db
from app.models.BusinessOrder import BusinessOrder as Order
from app.models.User import User

task_bk = Blueprint('api', __name__)

ENV = os.getenv('ENV') or 'production'
TASK_SERVER_KEY = os.getenv('TASK_SERVER_KEY')

servers = [
    "http://service01.w1.luyouxia.net",
    "http://server02.w1.luyouxia.net"
]


@task_bk.post('/update')
def update():
    data = request.get_json()
    oid = data['oid']
    status = data['status']
    order = Order.query.filter(Order.oid == oid).first()
    user = User.query.filter(User.uid == order.uid).first()

    # 更新订单数据和用户数据
    order.status = status
    if status == 203:
        user.balance += order.price
    elif status == 204:
        user.balance += order.price
    elif 400 <= status <= 499:
        pass
    elif 500 <= status <= 599:
        order.config = data['config']
        order.dtime = data['dtime']
    elif status >= 900:
        user.balance += order.price

    db.session.commit()
    return {"code": 1000, "msg": "ok"}


def send(oid, type, config):
    order = Order.query.filter(Order.oid == oid).first()
    rjson = {"code": 3000}
    for s in servers:
        resp = requests.post(url=s + '/accept',
                             data={'key': TASK_SERVER_KEY, 'oid': oid,
                                   'type': type, 'config': json.dumps(config)})
        try:
            rjson = resp.json()
        except:
            pass
        if rjson["code"] == 1000:
            order.callback = s;
            break
    else:
        order.status = 204
        User.query.filter(User.uid == order.uid).first().balance += order.price
        db.session.commit()
        return 1001
    db.session.commit()
    return 1000


def cancel(oid):
    order = Order.query.filter(Order.oid == oid).first()
    requests.post(url=order.callback + '/cancel',
                  data={'key': TASK_SERVER_KEY,
                        'oid': oid
                        })