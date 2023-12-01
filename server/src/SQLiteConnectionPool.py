from queue import Queue
from threading import Lock
import sqlite3
import os


class SQLiteConnectionPool:
    def __init__(self, db_path, max_connections):
        self.max_connections = max_connections
        self.db_path = db_path
        self.connections = Queue(maxsize=max_connections)
        self.lock = Lock()

    def get_conn(self):
        # 获取连接（游标）
        with self.lock:
            if self.connections.empty():
                # 如果连接池为空，创建新连接
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
            else:
                # 如果连接池不为空，获取可用连接
                conn = self.connections.get()
        return conn

    def release_conn(self, conn):
        # 释放连接
        with self.lock:
            if self.connections.qsize() < self.max_connections:
                # 如果连接池未满，将连接放回池中
                self.connections.put(conn)
            else:
                # 如果连接池已满，关闭连接
                conn.close()


class Cursor:
    """
    从连接池中获取连接，并返回该连接的游标对象。
    可使用上下文管理器安全地释放游标对象。
    """
    def __init__(self, pool):
        self.pool = pool
        self.conn = self.pool.get_conn()
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.commit()
        self.pool.release_conn(self.conn)
