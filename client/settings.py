from flask import Flask


def create_app():

    # 创建并配置app实例
    app = Flask(__name__)
    app.config.from_mapping({
        "SECRET_KEY": "dev",
        "DEBUG": True,
        "TESTING": True,
    })

    # 注册蓝图
    # import views.auth
    # app.register_blueprint(views.auth.bp)

    return app
