from .config import config
from .routes import routes
from .models import db

from flask import Flask
from flask_cors import CORS

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app, supports_credentials=True, origins=config[config_name].CORS_DOMAIN)
    db.init_app(app)

    for route in routes:    # 批量注册蓝图
        app.register_blueprint(route)

    return app
