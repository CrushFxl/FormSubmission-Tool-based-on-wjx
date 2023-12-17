import functools
from flask import session, redirect


def login_required(func):
    @functools.wraps(func)
    def inner():
        uid = session.get('uid')
        if uid:
            return func()
        else:
            return {"code": 3000, "msg": "登陆身份已过期，请重新登陆"}
    return inner
