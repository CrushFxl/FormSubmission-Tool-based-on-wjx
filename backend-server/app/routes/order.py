import random
import re
import time

import cv2
import numpy as np
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, request, session

from app.models import to_json
from app.routes.filters import login_required
from app.models import db
from app.models.User import User
from app.models.Order import Order

order_bk = Blueprint('order', __name__, url_prefix='/order')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


@order_bk.post('/query')
@login_required
def query():
    uid = session.get('uid')
    oid = request.form.get('oid')
    order = Order.query.filter(Order.oid==oid, Order.uid==uid).first()
    if order:
        return {"code": 1000, "order": order.to_json()}
    return {"code": 1001}


@order_bk.post('/wjx/pre')
@login_required
def wjx_pre():

    # 检查上传的图片
    if 'file' not in request.files:
        return {"code": 1001}
    try:
        file_bytes = request.files['file'].read()  # 转二进制流
        file_array = np.array(bytearray(file_bytes), dtype='uint8')  # 转数组
        img = cv2.imdecode(file_array, cv2.IMREAD_UNCHANGED)  # 转cv2对象
        ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY);  # 图像二值化
        det = cv2.QRCodeDetector()  # 检测二维码
        wjx_url, pts, st_code = det.detectAndDecode(img)  # 返回url结果
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

    # 生成订单信息
    current_time = time.localtime()
    uid = session.get('uid')
    oid = (str(int(time.time() * 1000)) + '01'
           + str(uid)[-3:] + str(random.randint(10, 99)))
    type = "wjx"
    state = "待付款"
    ctime = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    user = User.query.filter(User.uid==uid).first()
    info = dict({
        "url": wjx_url,
        "title": soup.title.text,
        "time": f"{y}-{int(M):02d}-{int(d):02d} {int(h):02d}:{int(m):02d}:00",
        "wjx_set": user.wjx_set,
        "option": ['标准']
    })
    price = 0.5

    # 写入数据库
    # noinspection PyArgumentList
    order = Order(oid=oid, uid=uid, type=type, state=state,
                  ctime=ctime, info=info, price=price)
    db.session.add(order)
    db.session.commit()
    return {"code": 1000, "order": to_json(order)}, 200


@order_bk.post('wjx/commit')
@login_required
def wjx_commit():
    uid = session.get('uid')
    oid = request.form.get('oid')
    user = User.query.filter(User.uid==uid).first()
    order = Order.query.filter(Order.uid==uid, Order.oid==oid).first()

    User.query.filter(User.uid==uid).with_for_update(read=False, nowait=False)  # 锁行
    if order.state != '待付款':
        return {"code": 1002}

    ctime = time.mktime(time.strptime(order.ctime, '%Y-%m-%d %H:%M:%S'))
    current_time = time.time()
    if current_time - ctime > 900:
        order.state = '已关闭'
        order.extra = 0
        db.session.commit()
        return {"code": 1003, "order": to_json(order)}

    if order.price > user.balance:
        return {"code": 1001, "msg": '付款失败，账户余额不足', "order": to_json(order)}
    User.query.filter(User.uid == uid).update({'balance': user.balance - order.price})
    order.ptime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    order.state = '进行中'
    db.session.commit()
    return {"code": 1000, "order": to_json(order)}

