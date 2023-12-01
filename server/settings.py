from src.SQLiteConnectionPool import SQLiteConnectionPool, Cursor
from flask import Flask
import os

# 设置数据库名称（存放于根目录下）
DB_NAME = "weactive.db"

# 数据库连接池最大连接数
MAX_CONNECTIONS = 10


def create_app():
    app = Flask(__name__)
    app.config.from_mapping({
        "SECRET_KEY": "dev",
        "DEBUG": True,
        "TESTING": True,
    })
    return app


def init_db():
    """
    :return: 数据库连接池对象
    """
    # 实例化数据库连接池
    path = os.path.dirname(__file__) + f"\\{DB_NAME}"
    pool = SQLiteConnectionPool(path, MAX_CONNECTIONS)

    # 创建数据表
    if not os.path.exists(path):
        with Cursor(pool) as c:

            # 定义User表
            c.execute('''CREATE TABLE users(
                        uid TEXT PRIMARY KEY NOT NULL,
                        phone TEXT NOT NULL,
                        password TEXT NOT NULL,
                        balance REAL NOT NULL);''')

            # 定义Register_cache表
            c.execute('''CREATE TABLE register_cache(
                        IP TEXT PRIMARY KEY NOT NULL,
                        try_times INT NOT NULL,
                        datetime TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        code INT NOT NULL);''')

    return pool
