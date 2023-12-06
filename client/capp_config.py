from flask import Flask

# 开发模式
DEBUG = True

# 连接的后端数据库服务器域名
SERVER_DOMAIN = "https://hmc.weactive.top:12345"


def create_app():
    app = Flask(__name__)
    if DEBUG:
        app.config.from_mapping({"DEBUG": True, "TESTING": True})
    else:
        app.config.from_mapping({"DEBUG": False, "TESTING": True})
    # import views.auth
    # app.register_blueprint(views.auth.bp)
    return app
