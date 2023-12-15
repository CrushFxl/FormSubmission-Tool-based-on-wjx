from .config import config
from .routes import routes

from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    for route in routes:    # 批量注册蓝图
        app.register_blueprint(route)

    return app
