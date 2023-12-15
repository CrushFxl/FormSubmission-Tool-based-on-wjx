import random
from flask import Blueprint, request, session
import time

from app.models import db
from app.models.User import User
from app.models.RegisterCache import RegisterCache as rCache
from app.api.aliyun_sms import send_sm

VALID_CHAR = ("0123456789ABCEDFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
              "!@#$%^&*()_+.-/<>,';:=`~|\\")

auth_bk = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bk.post('/')
def auth():
    uid = session.get('uid')
    if uid:
        return {'code': 1000, 'msg': 'ok'}
    return {'code': 1001, 'msg': '登陆身份已过期，请重新登陆'}


@auth_bk.post('/login')
def login():
    req = request.form.to_dict()
    user = User.query.filter(User.mob == req['mob'], User.pwd == req['pwd']).first()
    if user:
        session['uid'] = user.uid
        if req['keep'] == 'true':
            session.permanent = True
        return {"code": 1000, "msg": "ok"}
    return {"code": 1001, "msg": "用户名或密码错误"}


@auth_bk.post('/send')
def send():
    ip = request.remote_addr
    mob = int(request.form.get("mob"))
    ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # 检查是否满足注册条件
    if rCache.query.filter(rCache.ip == ip).count() >= 3:
        return {"code": 1001}
    if User.query.filter(User.mob == mob).first():
        return {"code": 1002}

    # 生成并发送验证码
    code = random.randint(123456, 987654)
    result = send_sm(mob, code)
    if result == "OK":
        register_cache = rCache(ip=ip, time=ctime, mob=mob, code=code)
        db.session.add(register_cache)
        db.session.commit()
        return {"code": 1000}
    else:
        return {"code": 2000, "msg": "接口内部错误：" + result}


@auth_bk.post('/register')
def register():
    mob = request.form.get("mob")
    code = int(request.form.get("code"))
    pwd = request.form.get("pwd")

    # 检查密码格式
    for i in pwd:
        if i not in VALID_CHAR:
            return {"code": 1001}
    if not 8 <= len(pwd) <= 18:
        return {"code": 1001}

    # 检查是否已被注册
    if User.query.filter(User.mob==mob).first():
        return {"code": 1002}

    # 检查注册信息
    rg_cache = rCache.query.filter(rCache.mob==mob, rCache.code==code).first()
    if rg_cache:
        time_stamp = time.mktime(time.strptime(rg_cache.time, '%Y-%m-%d %H:%M:%S'))
        current_time_stamp = time.time()
        if current_time_stamp - time_stamp < 300:
            # 生成唯一uid和sid
            while True:
                uid = random.randint(10000, 1000000000)
                if not User.query.filter(User.uid==uid).first():
                    break
            db.session.add(User(uid=uid, mob=mob, pwd=pwd))
            db.session.commit()
            session['uid'] = uid
            session.permanent = True
            return {"code": 1000}
    return {"code": 1003}
