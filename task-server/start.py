from flask import request
import cherrypy
import os

from server import app
from server.api import database, backend
from server.config import config as env_conf
from server.src.wjx import Taskwjx
from server.api.database import Task

with app.app_context():
    database.db.create_all()

ENV = os.getenv('ENV')
BACKEND_SERVER_DOMAIN = env_conf[ENV].BACKEND_SERVER_DOMAIN

def mkTask(oid, type, config, callback=1):
    # 验证订单转发次数
    if callback >= 8:  # 不要超过9，递归太深会报错
        backend.update(oid, 204, config)
        return {"code": 1000, "msg": "ok"}

    # 根据任务创建实例对象
    task = None
    if type == 'wjx':
        task = Taskwjx(oid, type, config)
    task.execute()


@app.post('/accept')
def accept():
    oid = request.form.get('oid')
    type = request.form.get('type')
    config = request.form.get('config')
    callback = int(request.form.get('callback'))
    mkTask(oid, type, config, callback)
    return {"code": 1000, "msg": "ok"}


if __name__ == '__main__':
    cherrypy.tree.graft(app.wsgi_app, '/')
    cherrypy.config.update(env_conf[ENV].CHERRYPY)
    cherrypy.engine.start()

    # 从本地读取任务
    with app.app_context():
        tasks = Task.query.filter(Task.status == 400).all()
        for t in tasks:
            mkTask(t.oid, t.type, t.config)

