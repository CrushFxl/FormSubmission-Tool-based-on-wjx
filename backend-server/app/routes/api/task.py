import json
import os
import random

import requests
from flask import Blueprint, request

from app.models import db
from app.models.BusinessOrder import BusinessOrder as Order
from app.models.User import User

task_bk = Blueprint('api', __name__)

ENV = os.getenv('ENV') or 'production'
TASK_SERVER_KEY = os.getenv('TASK_SERVER_KEY')


def getTaskServer():
    task_server_list = [
        "http://service01.w1.luyouxia.net"
    ]
    return random.choice(task_server_list)


@task_bk.post('/update')
def update():
    data = request.get_json()
    oid = data['oid']
    status = data['status']
    order = Order.query.filter(Order.oid == oid).first()
    user = User.query.filter(User.uid == order.uid).first()

    # 重新转发请求
    if status == 301:
        order.status = status
        order.callback += 1
        db.session.commit()
        send(oid, order.type, order.config, order.callback)
        return {"code": 1000, "msg": "ok"}

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

def send(oid, type, config, callback=1):
    requests.post(url=getTaskServer() + '/accept',
                  data={'key': TASK_SERVER_KEY,
                        'oid': oid,
                        'type': type,
                        'config': json.dumps(config),
                        'callback': callback
                        })


def cancel(oid):
    requests.post(url=getTaskServer() + '/cancel',
                  data={'key': TASK_SERVER_KEY,
                        'oid': oid
                        })
