from flask import Flask
import flasker.views.auth


def create_app():

    # 创建并配置app实例
    app = Flask(__name__)
    app.config.from_mapping({
        "SECRET_KEY": "dev",
        "DEBUG": True,
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    # 注册蓝图
    app.register_blueprint(flasker.views.auth.bp)

    return app
