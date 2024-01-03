import json

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
        self.status = 400                   # 任务状态
        self.config = json.loads(config)    # 任务配置

        # 添加本地数据库记录
        database.save(oid, type, config)

        # 通知后端已接单
        backend.update(oid, self.status)
