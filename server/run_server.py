"""
Python Required: 3.9.13
"""
from settings import init_app, init_db
from src.SMS_SDK import send_sm
from src.SQLiteConnectionPool import Cursor
from flask import request, make_response
import random
import time
import secrets

valid_chr = ("0123456789ABCEDFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
             "!@#$%^&*()_+.-/<>,';:=`~|\\")

app = init_app()
pool = init_db()


def login_required(func):
    def inner():
        uid = request.cookies.get('uid')


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
        if uid:    # 签发新的Cookie
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12345)
