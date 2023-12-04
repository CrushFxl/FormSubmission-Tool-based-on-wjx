from flask import Flask
import configparser
import os

Config = {}
settings_path = '\\'.join(os.path.dirname(__file__).split('\\')[:-1])+"\\settings.ini"
conf = configparser.ConfigParser()
conf.read(settings_path, encoding='utf-8-sig')
for k, v in conf["Config"].items():
    Config[k] = v


def create_app():
    # 创建并配置app实例
    app = Flask(__name__)
    app.config.from_mapping({
        "SECRET_KEY": "dev",
        "DEBUG": int(Config["debug"]),
        "TESTING": int(Config["testing"]),
    })
    # 注册蓝图
    # import views.auth
    # app.register_blueprint(views.auth.bp)
    return app
