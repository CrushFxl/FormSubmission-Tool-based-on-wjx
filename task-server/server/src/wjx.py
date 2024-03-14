import os
import random
import time

from playwright.sync_api import sync_playwright

from server.src import Task
from server.api import proxy

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}

class Taskwjx(Task):
    def __init__(self, oid, type, config):
        super().__init__(oid, type, config)
        self.url: str = self.config['url']       # 问卷网址

        # 代填设置
        self.set: list = [[k, v] for k, v in self.config['wjx_set'].items()]
        self.set.append(["联系方式", self.config['wjx_set']['手机']])
        self.remark: str = self.config['remark']  # 订单附加信息
        if self.remark:
            for i in self.remark.split(';'):
                self.set.append(i.split(":"))

        self.time: str = self.config['time']        # 报名开始时间
        self.result: dict = {}                      # 代填快照

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
        delay = starttime_stamp - nowtime_stamp - random.randint(25, 40)
        if delay < 0:
            self.status = 901
            raise AssertionError(f"活动已经开始或即将开始报名({delay})，无法执行")
        time.sleep(delay)

        with sync_playwright() as p:

            # 获取代理IP，启动浏览器
            ip = proxy.getIP()
            if os.getenv('ENV') == 'production':
                browser = p.chromium.launch(headless=True,
                                            proxy={'server': f'http://{ip}'})
            else:
                browser = p.chromium.launch(headless=False,
                                            proxy={'server': f'http://{ip}'})
            page = browser.new_page()
            page.goto(self.url)

            time.sleep(starttime_stamp - time.time() + 1)

            # 开始填写问卷
            try:
                next_btn = page.wait_for_selector('.button.mainBgColor')
                time.sleep(0.3)
                next_btn.click()
                submit_btn = page.wait_for_selector('#ctlNext')
                time.sleep(0.2)
                nodes = page.query_selector_all(".field.ui-field-contain")
            except:
                self.status = 903
                raise AssertionError(f"超时等待，订单发生预期之外的错误")

            for node in nodes:

                # 跳过非必填项
                req_node = node.query_selector('.req')
                if not req_node:
                    continue

                # 解析题目和题型
                text = node.query_selector('.topichtml').inner_text()   # 题干
                type_node = (node.query_selector_all('div:nth-child(2)'))[1]
                content = node.inner_html()     # 题型

                # 对于填空题
                if 'ui-input-text' in content:
                    for i in self.set:
                        if i[0] in text:
                            answer = i[1];
                            break
                    else:
                        answer = "1"    # 未知情况下填写
                    type_node.query_selector('input').fill(answer)
                    self.result[f'[填空题] {text}'] = answer

                # 对于单选题&多选题
                elif 'ui-controlgroup column1' in content:
                    options = []    # 选项内容列表
                    self.result[f'[选择题] {text}'] = ''   # 回答内容
                    option_text_node = type_node.query_selector_all('.label')
                    for i in option_text_node:
                        options.append(i.inner_text())
                    isFind = False
                    for i in self.set:
                        if i[0] in text:
                            for j in range(len(options)):
                                if i[1] in options[j]:
                                    tick = j;
                                    isFind = True
                                    option_text_node[tick].click()
                                    self.result[f'[选择题] {text}'] += options[tick]+';';
                    if not isFind:
                        if options[0] == '是':
                            tick = 0;
                        elif options[1] == '是':
                            tick = 1;
                        else:
                            tick = random.randint(0, len(options) - 1)
                        option_text_node[tick].click()
                        self.result[f'[选择题] {text}'] += options[tick]+';';

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
            self.config['wjx_result'] = self.result
            browser.close()
