"""
Python Required: 3.9.13
"""
import re

from settings import init_app, init_db, Config
from src.SMS_SDK import send_sm
from src.SQLiteConnectionPool import Cursor
from flask import request, make_response
from bs4 import BeautifulSoup
import requests
import random
import time
import secrets
import cv2
import numpy as np

valid_chr = ("0123456789ABCEDFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
             "!@#$%^&*()_+.-/<>,';:=`~|\\")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

app = init_app()
pool = init_db()


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


@app.post('/login/')
def login():
    # 验证携带的SID Cookie
    sid = request.cookies.get('sid')
    if sid:
        with Cursor(pool) as c:
            c.execute("SELECT uid FROM login_cache WHERE sid = ?", (sid,))
            uid = c.fetchone()
            if uid:
                return make_response({"Code": 1000, "UID": uid[0]}, 200)

    # 验证账号密码
    phoneNumber = request.form.get("Phone")
    password = request.form.get("Password")
    keep = request.form.get("Keep")
    with Cursor(pool) as c:
        c.execute("SELECT uid FROM users WHERE phone = ? AND password = ?",
                  (phoneNumber, password,))
        uid = c.fetchone()
        if uid:  # 签发新的Cookie
            sid = secrets.token_urlsafe(64)
            resp = make_response({"Code": 1000, "UID": uid[0]}, 200)
            if keep == "true":
                resp.set_cookie('sid', sid, max_age=31536000)
            else:
                resp.set_cookie('sid', sid)
            c.execute("REPLACE INTO login_cache(uid,sid) VALUES (?,?)", (uid[0], sid))
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


@app.post('/wjx/img/')
def wjx_img():
    # 读取传输的图片
    if 'file' not in request.files:
        return {"Code": 1001, "Message": "图片上传失败，请检查网络设置"}, 200

    # 识别图片中的二维码
    try:
        file_bytes = request.files['file'].read()  # 转二进制流
        file_array = np.array(bytearray(file_bytes), dtype='uint8')  # 转数组
        img = cv2.imdecode(file_array, cv2.IMREAD_UNCHANGED)  # 转cv2对象
        ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY);  # 图像二值化
        det = cv2.QRCodeDetector()  # 检测二维码
        wjx_url, pts, st_code = det.detectAndDecode(img)  # 返回url结果
    except cv2.error:
        return {"Code": 1002, "Message": "上传的文件类型无法识别"}, 200
    if wjx_url == '':
        return {"Code": 1003, "Message": "扫描不到二维码，换个清晰点的图片试试？"}, 200

    # 检查二维码的URL地址
    if "https://www.wjx." not in wjx_url:
        return {"Code": 1004, "Message": "二维码非问卷星网站，请检查图片是否正确"}, 200

    # 访问URL获取活动信息
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
    wjx_time = f"{y}年{M}月{d}日 {m}:00"
    wjx_title = soup.title.text
    return {"Code": 1000, "wjx_url": wjx_url, "wjx_title": wjx_title, "wjx_time": wjx_time}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(Config['server_ip'].split(':')[-1]))
