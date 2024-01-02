import os
import threading

import cherrypy
from flask import Flask
from flask_cors import CORS

from .config import config
from .routes import task_bp

ENV = os.getenv('ENV') or 'production'

def create_flask_app():
    app = Flask(__name__)
    app.config.from_object(config[ENV])
    CORS(app, supports_credentials=True)
    app.register_blueprint(task_bp)
    cherrypy.tree.graft(app.wsgi_app, '/')
    cherrypy.config.update(config[ENV].CHERRYPY)
