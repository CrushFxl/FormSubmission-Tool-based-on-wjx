import json
import os
import random
import re
import time
import cv2
import numpy as np
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, request, session
from sqlalchemy.orm.attributes import flag_modified

from app.routes.filters import login_required
from app.routes.api import task
from app.models import db
from app.models.User import User
from app.models.BusinessOrder import BusinessOrder as Order
business_order_bk = Blueprint('order', __name__, url_prefix='/order')

det = cv2.QRCodeDetector()
ENV = os.getenv('ENV') or 'production'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


@business_order_bk.post('/wjx/pre')
@login_required
def wjx_pre():
    # 检查上传的图片
    if 'file' not in request.files:
        return {"code": 1001}
    try:
        file_bytes = request.files['file'].read()  # 读二进制流
        file_array = np.frombuffer(file_bytes, np.uint8)  # 转np矩阵
        img = cv2.imdecode(file_array, cv2.IMREAD_COLOR)  # 转cv2对象
        ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY);  # 二值化处理
        wjx_url, pts, st_code = det.detectAndDecode(img)  # 扫描二维码
    except cv2.error:
        return {"code": 1002, "msg": "上传的文件类型无法识别"}
    if wjx_url == '':
        return {"code": 1003, "msg": "扫描不到二维码，用更清晰的图片试试吧"}
    if "https://www.wjx." not in wjx_url:
        return {"code": 1004, "msg": "非问卷星二维码，请检查图片是否正确"}

    # 数据预处理
    res = requests.get(wjx_url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    sttime = soup.find(id="divstarttime")
    if sttime is None:
        return {"code": 1005, "msg": "订单创建失败，此活动可能已开始报名或已结束报名，"
                                     "如果对此有疑问，请联系网站管理员。"}
    y, M, d, h = re.search(r"于(\d+)年(\d+)月(\d+)日 (\d+)点", sttime.text).groups()
    try:
        m = re.search(r"(\d+)分", sttime.text).groups()[0]
    except AttributeError:
        m = 0

    # 预生成订单信息
    current_time = time.localtime()
    uid = session.get('uid')
    oid = (str(int(time.time() * 1000)) + '01'
           + str(uid)[-3:] + str(random.randint(10, 99)))
    type = "wjx"
    ctime = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    config = dict({
        "url": wjx_url,
        "title": soup.title.text,
        "time": f"{y}-{int(M):02d}-{int(d):02d} {int(h):02d}:{int(m):02d}:00",
        "wjx_set": {},
        "wjx_result": []
    })

    # 计算订单价格
    options = [{"标准": 0.5}, {"内测用户优惠": -0.1}]
    price = 0
    for i in options:
        for k, v in i.items():
            price += v

    # 写入数据库
    order = Order(oid=oid, uid=uid, type=type, ctime=ctime, config=config,
                  options=options, price=price)
    db.session.add(order)
    db.session.commit()
    return {"code": 1000, "oid": oid}


@business_order_bk.post('wjx/commit')
@login_required
def wjx_commit():
    uid = session.get('uid')
    oid = request.form.get('oid')
    wjx_set = json.loads(request.form.get('wjx_set'))
    User.query.filter(User.uid == uid).with_for_update(read=False, nowait=False)  # 锁行

    user = User.query.filter(User.uid == uid).first()
    order = Order.query.filter(Order.uid == uid, Order.oid == oid).first()

    # 检查订单状态
    if order.status not in [0, 100]:
        return {"code": 1002, "msg": "当前订单正在进行或已被关闭，无法付款"}
    ctime = time.mktime(time.strptime(order.ctime, '%Y-%m-%d %H:%M:%S'))
    current_time = time.time()
    if current_time - ctime > 900:
        order.status = 200
        db.session.commit()
        return {"code": 1003, "msg": "由于长时间未支付，订单已自动关闭"}

    # 检查用户余额
    if order.price > user.balance:
        order.status = 100
        db.session.commit()
        return {"code": 1001, "msg": '付款失败，账户余额不足'}

    # 更新订单数据
    user.balance -= order.price  # 扣款
    user.ing += 1  # 进行中订单计数
    order.config['wjx_set'] = wjx_set  # 添加问卷星订单设置
    flag_modified(order, "config")  # (提交部分json的更改)
    order.ptime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 添加时间戳
    order.status = 300  # 修改订单状态（待接单）
    db.session.commit()
    task.send(oid, order.type, order.config)    # 将订单分发给业务服务器
    return {"code": 1000, 'msg': 'ok'}


@business_order_bk.post('/cancel')
@login_required
def cancel():
    uid = session.get('uid')
    oid = request.form.get('oid')
    User.query.filter(User.uid == uid).with_for_update(read=False, nowait=False)  # 锁行

    user = User.query.filter(User.uid == uid).first()
    order = Order.query.filter(Order.uid == uid, Order.oid == oid).first()

    status = str(order.status)[0]

    # 更新订单状态
    if status == '1':  # 待付款时
        order.status = 201
    elif status == '3':  # 排队中时
        user.ing -= 1
        order.status = 202
        user.balance += order.price
    elif status == '4':  # 进行中时
        order.status = 203
        user.ing -= 1
        user.balance += order.price
    else:  # 不允许退款
        return {"code": 1001, "msg": "当前订单不允许退款"}
    db.session.commit()

    return {"code": 1000, "msg": 'ok'}
