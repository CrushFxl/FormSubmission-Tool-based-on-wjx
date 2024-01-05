import json
import os
import requests
from flask import Blueprint, request

from app.routes.filters import signature_verify
from app.models import db
from app.config import config as env_conf
from app.models.BusinessOrder import BusinessOrder as Order
from app.models.User import User

task_bk = Blueprint('api', __name__)

ENV = os.getenv('ENV') or 'production'
TASK_SERVER_KEY = os.getenv('TASK_SERVER_KEY')
TASK_SERVER_DOMAIN = env_conf[ENV].TASK_SERVER_DOMAIN


@task_bk.post('/update')
def update():
    data = request.get_json()
    oid = data['oid']
    status = data['status']
    order = Order.query.filter(Order.oid == oid).first()
    user = User.query.filter(User.uid == order.uid).first()

    # 更新订单数据和用户数据
    order.status = status
    if 400 <= status <= 499:
        user.ing += 1
    elif 500 <= status <= 599:
        user.ing -= 1
        user.done += 1
        order.config = data['config']
        order.dtime = data['dtime']
    elif status >= 900:
        user.ing -= 1
        user.balance += order.price     # 退款

    db.session.commit()
    return {"code": 1000, "msg": "ok"}

def send(oid, type, config):
    requests.post(url=TASK_SERVER_DOMAIN + '/accept',
                  data={'key': TASK_SERVER_KEY,
                        'oid': oid,
                        'type': type,
                        'config': json.dumps(config)
                        })
