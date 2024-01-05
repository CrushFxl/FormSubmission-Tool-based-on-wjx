import random
import re
import time
import requests
from bs4 import BeautifulSoup
from pyppeteer import launch

from . import Task, headers

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive: true",
    "Dnt": "1",
    "Host": "www.wjx.cn",
    "Referer": "https://www.wjx.cn/newwjx/design/sendqstart.aspx?activity=239149328",
    "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}


class Taskwjx(Task):
    def __init__(self, oid, type, config):
        super().__init__(oid, type, config)
        self.url = self.config['url']  # 问卷网址
        self.set = self.config['wjx_set']  # 用户设置
        self.questions = []  # 问卷的题目
        self.answer = []  # 填写的答案
        self.stStamp = -1  # 问卷开始时间

    def run(self):
        try:
            self.getStartTimeStamp()
            self.waitUntilStart()
            self.getQuestions()
        except AssertionError as e:
            print(f"【错误】订单{self.oid}：{e}")
        else:
            # TODO: 更新wjx_result
            self.status = 500

    def getStartTimeStamp(self):
        res = requests.get(self.url, headers=headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        sttime = soup.find(id="divstarttime")
        if sttime is None:
            self.status = 901
            raise AssertionError("获取活动报名时间失败")
        y, M, d, h = re.search(r"于(\d+)年(\d+)月(\d+)日 (\d+)点", sttime.text).groups()
        try:
            m = re.search(r"(\d+)分", sttime.text).groups()[0]
        except AttributeError:
            m = 0
        date_time = time.strptime(f"{y}-{M}-{d} {h}:{m}", "%Y-%m-%d %H:%M")
        self.stStamp = int(time.mktime(date_time))

    async def waitUntilStart(self):
        browser = await launch(headless=True, dumpio=True, autoClose=False,
                               args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars'])  # 进入有头模式
        page = await browser.newPage()  # 打开新的标签页
        await page.goto(self.url)
        # await page.waitForSelector('.item .name')
        # names = [item.text() for item in doc('.item .name').items()]
        # await browser.close()
        nowtime_stamp = int(time.time())
        time.sleep(self.stStamp - nowtime_stamp)
        # TODO: 获取高匿ip

    def getQuestions(self):
        while True:
            resp = requests.get(self.url, headers=header)
            text = resp.text
            print("获取到啦", text)
            break


if __name__ == '__main__':
    task = Taskwjx("123", 'wjx', "a")
    task.url = "https://www.wjx.top/vm/rWAcLTu.aspx"
    task.execute()
