import functools
import os

from flask import request

TASK_SERVER_KEY = os.getenv('TASK_SERVER_KEY')


# 签名验证装饰器
def signature_verify(func):
    @functools.wraps(func)
    def inner():
        key = request.form.get('key')
        if key == TASK_SERVER_KEY:
            return func()
        else:
            return {"code": 3000, "msg": "拒绝访问"}
    return inner
