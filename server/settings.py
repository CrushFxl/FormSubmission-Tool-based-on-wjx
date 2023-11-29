from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    # 配置MySQL数据库
    HOSTNAME = "127.0.0.1"
    PORT = 3306
    USERNAME = "root"
    PASSWORD = "123456."
    DATABASE = "weactive"

    app = Flask(__name__)
    app.config.from_mapping({
        "SQLALCHEMY_DATABASE_URI": f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:"
                                   f"{PORT}/{DATABASE}?charset=utf8mb4",
        "SECRET_KEY": "dev",
        "DEBUG": True,
        "TESTING": True,
    })
    db = SQLAlchemy(app)
    # # 注册蓝图
    # import api.verify_inv_code
    # app.register_blueprint(api.verify_inv_code.bp)

    return app, db
