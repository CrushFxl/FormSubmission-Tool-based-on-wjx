from src.SQLiteConnectionPool import SQLiteConnectionPool, Cursor
from flask_cors import CORS
from datetime import timedelta
from flask import Flask
import configparser
import os

Config = {}
settings_path = '\\'.join(os.path.dirname(__file__).split('\\')[:-1])+"\\settings.ini"
conf = configparser.ConfigParser()
conf.read(settings_path, encoding='utf-8-sig')
for k, v in conf["Config"].items():
    Config[k] = v


def init_app():
    app = Flask(__name__)
    app.config.from_mapping({
        "DEBUG": int(Config["debug"]),
        "TESTING": int(Config["testing"]),
        "PERMANENT_SESSION_LIFETIME": timedelta(days=365),
    })

    # 允许clientURL携带Cookie跨域
    CORS(app, resources={"/*": {"origins": Config["client_ip"]}},
         supports_credentials=True)
    return app


def init_db():
    """
    :return: 数据库连接池对象
    """
    # 实例化数据库连接池
    db_path = os.path.dirname(__file__) + f"\\db"
    pool = SQLiteConnectionPool(db_path + f"\\{Config['db_name']}", int(Config["max_connections"]))

    # 创建数据表
    if not os.path.exists(db_path):
        os.makedirs(db_path)
        with Cursor(pool) as c:

            # 定义user表
            c.execute('''CREATE TABLE users(
                        uid TEXT PRIMARY KEY NOT NULL,
                        phone TEXT NOT NULL,
                        password TEXT NOT NULL,
                        balance REAL NOT NULL);''')

            # 定义register_cache表
            c.execute('''CREATE TABLE register_cache(
                        IP TEXT PRIMARY KEY NOT NULL,
                        try_times INT NOT NULL,
                        datetime TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        code INT NOT NULL);''')

            # 定义login_cache表
            c.execute('''CREATE TABLE login_cache(
                                    uid TEXT PRIMARY KEY NOT NULL,
                                    sid TEXT NOT NULL);''')

    return pool
