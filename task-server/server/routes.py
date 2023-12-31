import os
import json
from flask import Blueprint, request

from server.src.wjx import Task as Task_wjx

route_bp = Blueprint('route', __name__)

TASK_SERVER_KEY = os.getenv('TASK_SERVER_KEY')

@route_bp.post('/wjx')
def wjx():

    # 身份验证
    key = request.form.get('key')
    if key != TASK_SERVER_KEY:
        return {'code': 2000, 'msg': '拒绝访问'}

    # 任务实例化，开辟新线程
    oid = request.form.get('oid')
    config = json.loads(request.form.get('config'))
    Task_wjx(oid, config)

    return {'code': 1000, 'msg': 'ok'}
