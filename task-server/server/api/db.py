import sqlite3

from server.config import BaseConfig


def create_table():
    sql = """CREATE TABLE tasks (
                oid text primary key,
                config json not null,
                status integer not null DEFAULT 400
                );"""
    conn = sqlite3.connect(BaseConfig.DATABASE_PATH)
    cur = conn.cursor()
    try: cur.execute(sql)
    except sqlite3.OperationalError: pass
    cur.close()
    conn.close()


def accept_task(oid):
    conn = sqlite3.connect(BaseConfig.DATABASE_PATH)
    cur = conn.cursor()
    cur.close()
    conn.close()
