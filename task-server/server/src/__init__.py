import json
import os
import threading
import time
from abc import abstractmethod

from server import app
from server.api import database, backend
from server.api.database import Task as tTask

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

class Task:

    def __init__(self, oid, type, config):
        self.oid = oid                      # 任务订单号
        self.type = type                    # 任务类型
        self.config = json.loads(config)    # 任务配置
        self.status = 400                   # 任务状态
        self.dtime = '-'                    # 任务完成时间

    def execute(self):
        # 特判：检查问卷星任务并发量
        MAX_TASKS = int(os.getenv('MAX_TASKS') or 5)
        if self.type == 'wjx':
            if tTask.query.filter(tTask.unique == self.config['time'], tTask.status == 400).count() >= MAX_TASKS:
                backend.update(self.oid, 301)
                return

        if not tTask.query.filter(tTask.oid == self.oid).first():
            database.save(self.oid, self.type, json.dumps(self.config), str(self.config['time']))
            backend.update(self.oid, self.status)

        thd = threading.Thread(target=self.run)
        thd.start()

    @abstractmethod
    def run(self):
        pass

    def close(self):
        self.dtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # 更新本地数据库，同步后端数据库
        with app.app_context():
            database.update(self.oid, self.status)
        backend.update(self.oid, self.status, self.config, self.dtime)
