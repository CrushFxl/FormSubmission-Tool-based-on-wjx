from flask import request
import cherrypy
import os

from server import app
from server.api import database
from server.config import config
from server.src.wjx import Taskwjx

with app.app_context():
    database.db.create_all()    # 初始化数据库

ENV = os.getenv('ENV')
BACKEND_SERVER_DOMAIN = config[ENV].BACKEND_SERVER_DOMAIN


@app.post('/accept')
def accept():
    oid = request.form.get('oid')
    type = request.form.get('type')
    conf = request.form.get('config')

    # 创建任务实例对象
    task = Taskwjx(oid, type, conf)
    task.run()

    return {"code": 1000, "msg": "ok"}


if __name__ == '__main__':

    # 启动WSGI服务器
    cherrypy.tree.graft(app.wsgi_app, '/')
    cherrypy.config.update(config[ENV].CHERRYPY)
    cherrypy.engine.start()
