import os
import cherrypy
from flask import Flask
from flask_cors import CORS

from server.config import config
from server.routes import route_bp

ENV = os.getenv('ENV') or 'production'     # 读取上线环境


# 创建Flask App
app = Flask(__name__)
app.config.from_object(config[ENV])
app.register_blueprint(route_bp)
CORS(app, supports_credentials=True, origins=config[ENV].CORS_DOMAIN)


# 创建WSGI App
if __name__ == '__main__':
    conf = dict(app.config.items())
    cherrypy.tree.graft(app.wsgi_app, '/')
    cherrypy.config.update(conf['CHERRYPY'])
    cherrypy.engine.start()
