import os
import requests
from flask import Blueprint, request

from .config import config
from server.src.wjx import wjx_task
from .filters import signature_verify

task_bp = Blueprint('task', __name__)

BACKEND_SERVER_DOMAIN = config[os.getenv('ENV')].BACKEND_SERVER_DOMAIN


@task_bp.post('/accept')
def accept():
    oid = request.form.get('oid')
    conf = request.form.get('config')

    # 添加本地数据库记录
    pass

    # 创建任务实例对象
    wjx_task(oid, conf)

    # 通知后端修改数据库
    requests.post(url=BACKEND_SERVER_DOMAIN + '/service/accept', data={'oid': oid})
    return {"code": 1000, "msg": "ok"}
