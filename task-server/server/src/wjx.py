import json
import random
import time

import playwright
from playwright.sync_api import sync_playwright

from server.src import Task
from server.api import gpt
from server import app

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}

class Taskwjx(Task):
    def __init__(self, oid, type, config):
        super().__init__(oid, type, config)
        self.url: str = self.config['url']       # 问卷网址
        self.set: dict = self.config['wjx_set']   # 用户设置
        self.time: str = self.config['time']        # 报名开始时间
        self.remark: str = self.config['remark']    # 订单备注

    def run(self):
        try:
            self.signUpActivity()
        except AssertionError as e:
            print(f"【错误】订单{self.oid}：{e}")
        else:
            self.status = 500
        finally:
            self.close()

    def signUpActivity(self):

        # 线程挂起，直到报名开始前一分钟
        starttime_stamp = time.mktime(time.strptime(self.time, "%Y-%m-%d %H:%M:%S"))
        nowtime_stamp = time.time()
        delay = starttime_stamp - nowtime_stamp - random.randint(10, 60)
        if delay < 0:
            self.status = 901
            raise AssertionError(f"活动已经开始或即将开始报名({delay})，无法执行")
        time.sleep(delay)

        # 获取代理ip
        pass

        with sync_playwright() as p:

            # 报名开始后获取问卷内容
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(self.url)

            time.sleep(starttime_stamp - time.time() + 1)
            next_btn = page.wait_for_selector('.button.mainBgColor')
            time.sleep(1)
            next_btn.click()
            submit_btn = page.wait_for_selector('#ctlNext')
            nodes = page.query_selector_all(".field.ui-field-contain")

            for node in nodes:

                # 跳过非必填项
                req_node = node.query_selector('.req')
                if not req_node:
                    continue

                # 解析题目和题型
                text_node = node.query_selector('.topichtml')
                text = text_node.inner_text()   # 题干
                type_node = (node.query_selector_all('div:nth-child(2)'))[1]    # 选项
                content = node.inner_html()     # 题型

                # 对于填空题
                if 'ui-input-text' in content:
                    answer = None   # 本地匹配
                    for key in self.set.keys():
                        if key in text:
                            answer = self.set.get(key)
                    if not answer:  # 调用大模型获取答案
                        answer = gpt.getAnswer('【填空题】'+text, self.remark)
                    type_node.query_selector('input').fill(answer[:10])

                # 对于单选题&多选题
                elif 'ui-controlgroup column1' in content:
                    # 特判
                    if text == '性别' and self.set['性别'] in ['男', '女']:
                        page.get_by_text(self.set['性别']).click()
                        continue
                    # 解析选项
                    num = 0
                    options = []
                    options_text = ''
                    option_text_node = type_node.query_selector_all('.label')
                    for option in option_text_node:
                        num += 1
                        options.append(option.inner_text())
                        options_text += f"[{num}]{options[-1]}; "
                    # 大模型生成回答
                    if '【多选题】' in text:
                        answer = gpt.getAnswer('【多选题】' + text[:-5], self.remark, options_text)
                    else:
                        answer = gpt.getAnswer('【单选题】' + text, self.remark, options_text)
                    for i in range(1, num + 1):
                        if f"[{i}]" in answer:
                            page.get_by_text(options[i - 1]).click()

                # 对于未知类型
                else:
                    self.status = 910
                    raise AssertionError(f'遇到未知的问题类型：{content}')

            submit_btn.click()  # 点击提交按钮
            try:
                page.wait_for_selector('.submit_tip_color')
            except:
                self.status = 902
                raise AssertionError('提交问卷超时')

            page.close()
            time.sleep(5)
            browser.close()


if __name__ == '__main__':
    task = Taskwjx("123456", "wjx", json.dumps({
        "url": "https://www.wjx.cn/vm/evfoZuA.aspx",
        "wjx_set": {
            '班级': '魔法学院1年级3班',
            '姓名': '鲁迪',
            '学号': '6401230103'
        },
        "time": "2024-02-01 23:40:00",
        "remark": "选择上午时间段"
    }))
    with app.app_context():
        task.execute()
