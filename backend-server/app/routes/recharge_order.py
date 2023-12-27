import hashlib
import json
import os
import time
import random

import requests
from flask import Blueprint, request, session

from app.routes.filters import login_required
from app.models import db
from app.models.RechargeOrder import RechargeOrder as Order
from app.models.User import User

recharge_order_bk = Blueprint('recharge', __name__, url_prefix='/recharge')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

# 配置信息（注：支付接口只能在生产环境下测试）
app_id = 2312208768
H5PAY_KEY = os.getenv('H5PAY_KEY')
description = "WeActive充值订单"
notify_url = 'https://hmc.weactive.top:12345/recharge/callback'
out_trade_no = "123"


# 签名算法
def sign(attributes, key):
    attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
    sign_str = "&".join(
        [f"{key}={attributes_new[key]}" for key in attributes_new.keys()]
    )
    return (
        hashlib.md5((sign_str + "&key=" + key).encode(encoding="utf-8"))
        .hexdigest()
        .upper()
    )


# 接收订单支付成功通知
@recharge_order_bk.post('/callback')
def callback():
    # 验证签名
    oid = request.form.get('oid')
    order = Order.query.filter(Order.oid==oid).first()
    signed = request.form.get('sign')
    if order.sign != signed:
        return "拒绝访问"

    # 更新订单信息
    order.status = "paid"
    order.h5id = request.form.get("trade_no")
    order.payid = request.form.get("in_trade_no")
    order.ptime = request.form.get("pay_time")

    # 账户累加充值金额
    uid = order.uid
    amount = order.price
    User.query.filter(User.uid==uid).first().balance += amount
    print("\n\n\n已收到回调通知")
    return "success"


# 拉起支付接口
@recharge_order_bk.post('/')
@login_required
def commit():
    uid = session.get('uid')
    amount = int(request.form.get('price')) * 100
    env = request.form.get('env')
    pay_type = request.form.get('payment')

    # 组装数据
    data = {
        "app_id": app_id,
        "out_trade_no": out_trade_no,
        "description": description,
        "pay_type": pay_type,
        "amount": amount,
        "notify_url": notify_url,
    }
    signed = sign(data, key=H5PAY_KEY)  # 进行签名
    data['sign'] = signed

    # 请求拉起支付接口
    resp = requests.post('https://open.h5zhifu.com/api/' + env,
                         headers=headers,
                         data=json.dumps(data))
    resp = resp.json()
    if resp["msg"] != "success" or resp['code'] != 200:
        print(resp['msg'])
        return {"code": 1001,
                "msg": "拉起支付接口失败，内部错误代码："+str(resp['code'])}

    # 生成支付订单
    current_time = time.localtime()
    oid = (str(int(time.time() * 1000)) + '00'
           + str(uid)[-3:] + str(random.randint(10, 99)))
    ctime = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    order = Order(oid=oid, uid=uid, payment=pay_type,
                  price=amount/100, ctime=ctime, sign=signed)
    db.session.add(order)
    db.session.commit()

    # 返回支付地址
    jump_url = resp['jump_url']
    print(resp, "\n\n\n已生成支付订单")
    return {"code": 1000, "msg": "ok", "url": jump_url}
