from settings import create_app, init_db
from src.SMS_SDK import send_sm
from src.SQLiteConnectionPool import Cursor
from flask import request
import random
import time

valid_chr = "0123456789ABCEDFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+.-/<>,';:=`~|\\"
origin = {"Access-Control-Allow-Origin": "*"}

app = create_app()  # 初始化Flask应用
pool = init_db()  # 初始化数据库，并创建数据库连接池对象


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
                return {"Code": 1001}, 200, origin
            try_times += record[1]

        # 后端格式检查
        for i in phoneNumber:
            if i not in "0123456789":
                return {"Code": 1003}, 200, origin
        if len(phoneNumber) != 11:
            return {"Code": 1003}, 200, origin

        # 检查是否已被注册
        c.execute("SELECT * FROM users WHERE phone = ?", (phoneNumber,))
        existed = c.fetchone()
        if existed:
            return {"Code": 1002}, 200, origin

        # 生成并发送验证码
        code = random.randint(123456, 987654)
        result = send_sm(phoneNumber, code)
        if result == "OK":
            c.execute("REPLACE INTO register_cache (IP,try_times,datetime,phone,code) "
                      "VALUES (?,?,?,?,?)", (IP, try_times, datetime, phoneNumber, code))
            return {"Code": 1000}, 200, origin
        else:
            print("接口内部错误", result)
            return {"Code": 2000, "Message": result}, 200, origin


@app.post('/register/')
def register():
    phoneNumber = request.form.get("Phone")
    code = int(request.form.get("Code"))
    password = request.form.get("Password")

    # 后端密码格式验证
    for i in password:
        if i not in valid_chr:
            return {"Code": 1001}, 200, origin
    if not 8<=len(password)<=18:
        return {"Code": 1001}, 200, origin

    with Cursor(pool) as c:

        # 检查是否已被注册
        c.execute("SELECT * FROM users WHERE phone = ?", (phoneNumber,))
        existed = c.fetchone()
        if existed:
            return {"Code": 1003}, 200, origin

        # 核验短信验证码
        c.execute("SELECT * FROM register_cache WHERE phone = ?", (phoneNumber,))
        record = c.fetchone()
        if record:
            time_stamp = time.mktime(time.strptime(record[2], '%Y-%m-%d %H:%M:%S'))
            correct_code = record[4]
            current_time_stamp = time.time()
            if correct_code == code and current_time_stamp - time_stamp < 300:
                while True:     # 生成唯一用户uid
                    uid = random.randint(10000, 100000000)
                    c.execute("SELECT * FROM users WHERE uid = ?", (uid,))
                    if not c.fetchone():
                        break
                c.execute("INSERT INTO users(uid,phone,password,balance) VALUES (?,?,?,?)",
                          (uid, phoneNumber, password, 1.00))
                return {"Code": 1000}, 200, origin
    return {"Code": 1002}, 200, origin


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12345)
