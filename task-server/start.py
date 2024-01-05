from flask import request
import cherrypy
import os

from server import app
from server.api import database
from server.config import config as env_conf
from server.src.wjx import Taskwjx

with app.app_context():
    database.db.create_all()

ENV = os.getenv('ENV')
BACKEND_SERVER_DOMAIN = env_conf[ENV].BACKEND_SERVER_DOMAIN


@app.post('/accept')
def accept():
    oid = request.form.get('oid')
    type = request.form.get('type')
    config = request.form.get('config')

    # 根据任务创建实例对象
    task = None
    if type == 'wjx':
        task = Taskwjx(oid, type, config)
    task.execute()

    return {"code": 1000, "msg": "ok"}


if __name__ == '__main__':
    cherrypy.tree.graft(app.wsgi_app, '/')
    cherrypy.config.update(env_conf[ENV].CHERRYPY)
    cherrypy.engine.start()
