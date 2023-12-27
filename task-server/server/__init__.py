from .config import config
from .src import routes

from flask import Flask
from flask_cors import CORS

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app, supports_credentials=True, origins=config[config_name].CORS_DOMAIN)

    for route in routes:
        app.register_blueprint(route)   # 批量注册蓝图

    return app
