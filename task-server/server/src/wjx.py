import re
import threading
import time
import requests
from bs4 import BeautifulSoup

from . import Task, headers
from server.api import database
from server.api import backend
from server import app


class Taskwjx(Task):
    def __init__(self, oid, type, config):
        super().__init__(oid, type, config)
        self.tStamp = None    # 开始报名时间戳

    # 获取开始报名时间戳
    def getTimeStamp(self):
        url = self.config['url']
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        sttime = soup.find(id="divstarttime")
        if sttime is None:
            self.status = 901
            raise AssertionError("获取问卷时间时发生错误")
        y, M, d, h = re.search(r"于(\d+)年(\d+)月(\d+)日 (\d+)点", sttime.text).groups()
        try:
            m = re.search(r"(\d+)分", sttime.text).groups()[0]
        except AttributeError:
            m = 0
        date_time = time.strptime(f"{y}-{M}-{d} {h}:{m}", "%Y-%m-%d %H:%M")
        self.tStamp = int(time.mktime(date_time))
        return 0

    def run(self):
        def _run():
            try:
                self.getTimeStamp()
            except AssertionError as e:
                print(f"【错误】订单{self.oid}：{e}")
            finally:
                with app.app_context():
                    database.update(self.oid, self.status)    # 更新本地数据库
                backend.update(self.oid, self.status)   # 更新后端数据库

        thd = threading.Thread(target=_run)
        thd.start()
