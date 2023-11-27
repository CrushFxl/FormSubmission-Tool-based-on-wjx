from flask import Flask


def create_app():
    # 创建并配置app实例
    app = Flask(__name__)
    app.config.from_mapping({

        # 数据库配置
        "SQLALCHEMY_DATABASE_URI": "",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,

        "SECRET_KEY": "dev",
        "DEBUG": True,
        "TESTING": True,
    })

    # 默认允许的跨源访问地址
    app.config["origin"] = {"Access-Control-Allow-Origin": "*"}

    # 注册蓝图
    import api.verify_inv_code
    app.register_blueprint(api.verify_inv_code.bp)

    return app
