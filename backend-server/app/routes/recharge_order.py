import hashlib
import json
import os
import re
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
notify_url = 'https://api.weactive.top/recharge/callback'


# 签名算法
def sign(attributes, key):
    attributes_new = {k: attributes[k] for k in sorted(attributes.keys()) if attributes[k]}
    sign_str = "&".join(
        [f"{key}={attributes_new[key]}" for key in attributes_new.keys()]
    )
    return (
        hashlib.md5((sign_str + "&key=" + key).encode(encoding="utf-8"))
        .hexdigest()
        .upper()
    )


# 拉起支付接口
@recharge_order_bk.post('/')
@login_required
def commit():
    uid = session.get('uid')
    amount = int(request.form.get('price')) * 100
    env = request.form.get('env')
    pay_type = request.form.get('payment')

    # 组装数据
    oid = str(int(time.time() * 1000)) + '00' + str(uid)[-3:] + str(random.randint(10, 99))
    data = {
        "app_id": app_id,
        "out_trade_no": oid,
        "description": description,
        "pay_type": pay_type,
        "amount": amount,
        "notify_url": notify_url,
    }

    # 进行签名
    signed = sign(data, key=H5PAY_KEY)
    data['sign'] = signed

    # 请求拉起支付跳转
    resp = requests.post('https://open.h5zhifu.com/api/' + env,
                         headers=headers,
                         data=json.dumps(data))
    resp = resp.json()
    if resp['msg'] != "success" or resp['code'] != 200:
        return {"code": 1001,
                "msg": "拉起支付接口失败，内部错误代码：" + str(resp['code'])}

    # 生成支付订单
    h5id = resp['data']['trade_no']
    ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    order = Order(oid=oid, h5id=h5id, uid=uid, payment=pay_type, price=amount / 100, ctime=ctime)
    db.session.add(order)
    db.session.commit()

    # 解析跳转中间页，少掉一层跳转，拿到DeepLink
    jump_url = resp['data']['jump_url']
    h5_resp = requests.get(jump_url, headers=headers)
    wx_url = re.search(r'top.location.href = "(.*?)"', h5_resp.text).groups()[0]
    headers['Referer'] = 'https://service-bejmsi0z-1252021128.sh.apigw.tencentcs.com/'  # 伪装请求头
    wx_resp = requests.get(wx_url, headers=headers)
    deep_link = re.findall(r'deeplink : "(.*?)"', wx_resp.text)[1]
    return {"code": 1000, "msg": "ok", "deep_link": deep_link, "oid": oid}


# 接收订单支付成功通知
@recharge_order_bk.post('/callback')
def callback():
    # 验证签名
    req = request.get_json()
    received_sign = req['sign']
    req['sign'] = ''
    correct_sign = sign(req, H5PAY_KEY)
    if correct_sign != received_sign:
        return "拒绝访问"

    # 更新订单信息
    oid = req['out_trade_no']
    order = Order.query.filter(Order.oid == oid).first()
    if order.status == "wait":
        order.status = "paid"
        order.h5id = req["trade_no"]
        order.payid = req["in_trade_no"]
        order.ptime = req["pay_time"]
    else:
        return "success"  # 防止重复通知

    # 账户累加充值金额
    uid = order.uid
    amount = order.price
    User.query.filter(User.uid == uid).first().balance += amount
    db.session.commit()
    return "success"
