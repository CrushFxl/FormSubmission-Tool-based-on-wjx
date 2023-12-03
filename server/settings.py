from src.SQLiteConnectionPool import SQLiteConnectionPool, Cursor
from flask_cors import CORS
from datetime import timedelta
from flask import Flask
import configparser
import os

clientURL = "http://127.0.0.1"

# 从SecretKey.ini中读取所有密钥信息
path = os.path.dirname(__file__)
conf = configparser.ConfigParser()
conf.read(path+f"\\SecretKey.ini", encoding='utf-8-sig')
Ali_ACCESS_KEY_ID = conf["Ali_AccessKey"]["access_key_id"]
Ali_ACCESS_KEY_SECRET = conf["Ali_AccessKey"]["access_key_secret"]
FLASK_SECRET_KEY = conf["Flask_SecretKey"]["secret_key"]

# 设置数据库sqlite3
DB_NAME = "weactive.db"
MAX_CONNECTIONS = 10


def init_app():
    app = Flask(__name__)
    app.config.from_mapping({
        "SECRET_KEY": FLASK_SECRET_KEY,
        "DEBUG": True,
        "TESTING": True,
        "PERMANENT_SESSION_LIFETIME": timedelta(days=365),
        "SESSION_COOKIE_SAMESITE": "Lax"
    })
    # 允许clientURL跨域
    CORS(app, supports_credentials=True, origins=clientURL)
    return app


def init_db():
    """
    :return: 数据库连接池对象
    """
    # 实例化数据库连接池
    db_path = os.path.dirname(__file__) + f"\\db"
    pool = SQLiteConnectionPool(db_path + f"\\{DB_NAME}", MAX_CONNECTIONS)

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
