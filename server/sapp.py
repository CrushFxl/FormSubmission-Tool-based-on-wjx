"""
Python Required: 3.9.13
"""
import json

from sapp_config import init_app, init_db, DEV
from src.SMS_SDK import send_sm
from src.SQLiteConnectionPool import Cursor
from flask import request, make_response, jsonify
from bs4 import BeautifulSoup
import requests
import random
import time
import secrets
import cv2
import re
import numpy as np

WJX_BASIC_PRICE = 0.5  # 问卷星代抢服务基础定价

valid_chr = ("0123456789ABCEDFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
             "!@#$%^&*()_+.-/<>,';:=`~|\\")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

app = init_app()
pool = init_db()


def sid2uid(sid):
    with Cursor(pool) as c:
        c.execute("SELECT uid FROM login_cache WHERE sid = ?", (sid,))
        uid = c.fetchone()
        if uid:
            return uid[0]
        else:
            return None


@app.post('/phone/')
def phone():
    try_times = 1
    IP = request.remote_addr
    datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    phoneNumber = request.form.get("Phone")

    with Cursor(pool) as c:

        # 检查请求次数
        c.execute("SELECT * FROM register_cache WHERE IP = ?", (IP,))
        record = c.fetchone()
        if record:
            if record[1] >= 3:
                return {"Code": 1001}, 200
            try_times += record[1]

        # 后端格式检查
        for i in phoneNumber:
            if i not in "0123456789":
                return {"Code": 1003}, 200
        if len(phoneNumber) != 11:
            return {"Code": 1003}, 200

        # 检查是否已被注册
        c.execute("SELECT * FROM users WHERE phone = ?", (phoneNumber,))
        existed = c.fetchone()
        if existed:
            return {"Code": 1002}, 200

        # 生成并发送验证码
        code = random.randint(123456, 987654)
        result = send_sm(phoneNumber, code)
        if result == "OK":
            c.execute("REPLACE INTO register_cache (IP,try_times,datetime,phone,code) "
                      "VALUES (?,?,?,?,?)", (IP, try_times, datetime, phoneNumber, code))
            return {"Code": 1000}, 200
        else:
            print("接口内部错误", result)
            return {"Code": 2000, "Message": result}, 200


@app.post('/register/')
def register():
    phoneNumber = request.form.get("Phone")
    code = int(request.form.get("Code"))
    password = request.form.get("Password")

    # 后端密码格式验证
    for i in password:
        if i not in valid_chr:
            return {"Code": 1001}, 200
    if not 8 <= len(password) <= 18:
        return {"Code": 1001}, 200

    with Cursor(pool) as c:

        # 检查是否已被注册
        c.execute("SELECT * FROM users WHERE phone = ?", (phoneNumber,))
        existed = c.fetchone()
        if existed:
            return {"Code": 1003}, 200

        # 核验短信验证码
        c.execute("SELECT * FROM register_cache WHERE phone = ?", (phoneNumber,))
        record = c.fetchone()
        if record:
            time_stamp = time.mktime(time.strptime(record[2], '%Y-%m-%d %H:%M:%S'))
            correct_code = record[4]
            current_time_stamp = time.time()
            if correct_code == code and current_time_stamp - time_stamp < 300:
                # 生成唯一uid和sid
                while True:
                    uid = random.randint(10000, 100000000)
                    c.execute("SELECT * FROM users WHERE uid = ?", (uid,))
                    if not c.fetchone():
                        break
                sid = secrets.token_urlsafe(64)
                # 数据库注册
                c.execute("INSERT INTO users(uid,phone,password,balance) VALUES (?,?,?,?)",
                          (uid, phoneNumber, password, 1.00))
                c.execute("INSERT INTO login_cache(uid,sid) VALUES (?,?)", (uid, sid))
                # 返回cookie
                resp = make_response({"Code": 1000}, 200)
                resp.set_cookie('sid', sid, max_age=31536000)
                return resp
    return {"Code": 1002}, 200


@app.post('/verify/')
def verify():
    # 验证携带的SID Cookie
    sid = request.cookies.get('sid')
    if sid2uid(sid):
        return make_response({"Code": 1000}, 200)
    return make_response({"Code": 1001}, 200)


@app.post('/login/')
def login():
    # 验证账号密码
    phoneNumber = request.form.get("Phone")
    password = request.form.get("Password")
    keep = request.form.get("Keep")
    with Cursor(pool) as c:
        c.execute("SELECT * FROM users WHERE phone = ? AND password = ?",
                  (phoneNumber, password,))
        record = c.fetchone()
        if record:  # 签发新的Cookie
            uid = record[0]
            sid = secrets.token_urlsafe(64)
            resp = make_response({"Code": 1000}, 200)
            if keep == "true":
                resp.set_cookie('sid', sid, max_age=31536000)
            else:
                resp.set_cookie('sid', sid)
            c.execute("REPLACE INTO login_cache(uid,sid) VALUES (?,?)", (uid, sid))
            return resp
    return make_response({"Code": 1001}, 200)


@app.post('/logout/')
def logout():
    sid = request.cookies.get('sid')
    if sid:
        with Cursor(pool) as c:
            c.execute("DELETE FROM login_cache WHERE sid = ?", (sid,))
        return {"Code": 1000}, 200
    return {"Code": 1001}, 200


@app.post('/orders_query/')
def orders_query():
    sid = request.cookies.get('sid')
    uid = sid2uid(sid)
    if not uid:
        return {"Code": 2000, "Message": "登陆状态异常，请刷新网页后重试"}, 200

    # 组装数据
    orders = {}
    with Cursor(pool) as c:
        c.execute("SELECT * FROM orders WHERE uid =  (?) limit 10", (uid,))
        records = c.fetchall()
        for record in records:
            del record[1]  # 删除uid
            if record[3]:
                print(record[3])

    return {"Code": 1000}, 200


@app.post('/wjx_order_pre/')
def wjx_order_pre():
    sid = request.cookies.get('sid')
    uid = sid2uid(sid)
    if not uid:
        return {"Code": 2000, "Message": "登陆状态异常，请刷新网页后重试"}, 200
    if 'file' not in request.files:
        return {"Code": 1001, "Message": "图片上传失败，请检查网络设置"}, 200

    # # API扫描二维码
    # api_url = ("https://sapi.k780.com/?app=qr.read&datas=&datas_format=base64&"
    #            "appkey=71526&sign=bea97985a151663b0eb5556eec1943d6")
    # resp = requests.post(api_url)
    # print(resp.text,type(resp.text))

    # 扫描图片
    try:
        file_bytes = request.files['file'].read()  # 转二进制流
        file_array = np.array(bytearray(file_bytes), dtype='uint8')  # 转数组
        img = cv2.imdecode(file_array, cv2.IMREAD_UNCHANGED)  # 转cv2对象
        ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY);  # 图像二值化
        det = cv2.QRCodeDetector()  # 检测二维码
        wjx_url, pts, st_code = det.detectAndDecode(img)  # 返回url结果
        # cv2.imshow('Image', img)
        #
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    except cv2.error:
        return {"Code": 1002, "Message": "上传的文件类型无法识别"}, 200
    if wjx_url == '':
        return {"Code": 1003, "Message": "扫描不到二维码，换个清晰点的图片试试？"}, 200
    if "https://www.wjx." not in wjx_url:
        return {"Code": 1004, "Message": "二维码非问卷星网站，请检查图片是否正确"}, 200

    # 数据预处理
    res = requests.get(wjx_url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    sttime = soup.find(id="divstarttime")
    if sttime is None:
        return {"Code": 1005, "Message": "订单创建失败，此活动可能已开始报名或已结束报名，"
                                         "如果对此有疑问，请联系网站管理员。"}, 200
    y, M, d, h = re.search(r"于(\d+)年(\d+)月(\d+)日 (\d+)点", sttime.text).groups()
    try:
        m = re.search(r"(\d+)分", sttime.text).groups()[0]
    except AttributeError:
        m = 0
    nowtime = time.localtime()
    with Cursor(pool) as c:
        c.execute("SELECT wjx_set FROM users WHERE uid = ?", (uid,))
        wjx_set = json.loads(c.fetchone()[0])

    # 生成订单信息
    oid = str(int(time.time() * 1000)) + '01' + str(uid)[-3:] + str(random.randint(10, 99))
    uid = uid
    state = "待付款"
    ctime = time.strftime('%Y-%m-%d %H:%M:%S', nowtime)
    info = dict({
        "wjx_url": wjx_url,
        "wjx_title": soup.title.text,
        "wjx_time": f"{y}-{int(M):02d}-{int(d):02d} {int(h):02d}:00:00",
        "wjx_set": wjx_set,
        "wjx_option": []
    })
    price = 0.5
    # 写入数据库
    with Cursor(pool) as c:
        c.execute("INSERT INTO orders(oid,uid,state,ctime,info,price) VALUES (?,?,?,?,?,?)",
                  (oid, uid, state, ctime, str(info), price))
    order = {"oid": oid, "uid": uid, "state": state, "ctime": ctime, "info": info, "price": price}
    return {"Code": 1000, "order": order}, 200


@app.post('/wjx_order_buy/')
def wjx_order_buy():
    sid = request.cookies.get('sid')
    uid = sid2uid(sid)
    if not uid:
        return {"Code": 2000, "Message": "登陆状态异常，请刷新网页后重试"}, 200
    with Cursor(pool) as c:
        c.execute("SELECT balance FROM users WHERE uid =  (?)", (uid,))
        balance = c.fetchone()[0]
    return make_response({"Code": 1000}, 200)


@app.post('/wjx_set/')
def wjx_set_set():
    sid = request.cookies.get('sid')
    uid = sid2uid(sid)
    if uid:
        with Cursor(pool) as c:
            wjxset = request.form.get("wjx_set")
            c.execute("UPDATE users SET wjx_set = (?) WHERE uid =  (?)", (wjxset, uid))
        return make_response({"Code": 1000}, 200)
    return make_response({"Code": 1001}, 200)


if __name__ == "__main__":
    if DEV:
        app.run(host="0.0.0.0", port=12345)
    else:
        app.run(host="0.0.0.0", port=12345,
                ssl_context=('./SSL/hmc.weactive.top.pem', './SSL/hmc.weactive.top.key'))
