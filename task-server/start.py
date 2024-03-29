import json

from flask import request
import cherrypy
import os

from server import app
from server.api import database
from server.config import config as env_conf
from server.src.wjx import Taskwjx
from server.api.database import Task, db

with app.app_context():
    database.db.create_all()

ENV = os.getenv('ENV')
MAX_TASKS = int(os.getenv('MAX_TASKS') or 5)
BACKEND_SERVER_DOMAIN = env_conf[ENV].BACKEND_SERVER_DOMAIN

@app.post('/accept')
def accept():
    oid = request.form.get('oid')
    type = request.form.get('type')
    config = request.form.get('config')
    jsoned_config = json.loads(config)
    if Task.query.filter(Task.unique == jsoned_config['time'],
                         Task.status == 400).count() >= MAX_TASKS:
        return {"code": 1001}
    ptask = Taskwjx(oid, type, config)
    ptask.execute()
    return {"code": 1000, "msg": "ok"}

# 修改问卷星订单配置
@app.post('/modify_remark')
def modify_remark():
    oid = request.form.get('oid')
    new_remark = request.form.get('remark')
    ptask = Task.query.filter(Task.oid == oid).first()
    ptask.config = json.loads(new_remark)
    db.session.commit()
    return {"code": 1000, "msg": "ok"}


if __name__ == '__main__':
    cherrypy.tree.graft(app.wsgi_app, '/')
    cherrypy.config.update(env_conf[ENV].CHERRYPY)
    # if os.getenv('ENV') == 'production':
    #     cherrypy.server.ssl_certificate = "certs/service01.weactive.top.pem"
    #     cherrypy.server.ssl_private_key = "certs/service01.weactive.top.key"
    cherrypy.engine.start()

    # 从本地读取任务
    with app.app_context():
        tasks = Task.query.filter(Task.status == 400).all()
        for t in tasks:
            task = Taskwjx(t.oid, t.type, t.config)
            task.execute()