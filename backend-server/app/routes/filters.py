import functools
import os
from flask import session, request


TASK_SERVER_KEY = os.getenv('TASK_SERVER_KEY')


# 验证前端的身份
def login_required(func):
    @functools.wraps(func)
    def inner():
        uid = session.get('uid')
        if uid:
            return func()
        else:
            return {"code": 3000, "msg": "登陆身份已过期，请重新登陆"}
    return inner


# 验证业务端的身份
def signature_verify(func):
    @functools.wraps(func)
    def inner():
        key = request.form.get('key')
        if key == TASK_SERVER_KEY:
            return func()
        else:
            return {"code": 3000, "msg": "拒绝访问"}
    return inner
