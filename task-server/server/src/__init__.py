import json
import threading
import time
from abc import abstractmethod

from server import app
from server.api import database, backend

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

        database.save(oid, type, config)    # 添加本地数据库记录
        backend.update(oid, self.status)    # 通知后端已接单

    def execute(self):
        thd = threading.Thread(target=self.run)
        thd.start()

    @abstractmethod
    def run(self):
        pass

    def __del__(self):
        self.dtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # 更新本地数据库，同步后端数据库
        with app.app_context():
            database.update(self.oid, self.status)
        backend.update(self.oid, self.status, self.config, self.dtime)
