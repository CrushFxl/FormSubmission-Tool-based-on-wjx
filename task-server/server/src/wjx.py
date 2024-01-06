import random
import time

from playwright.sync_api import sync_playwright

from server.src import Task

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}


class Taskwjx(Task):
    def __init__(self, oid, type, config):
        super().__init__(oid, type, config)
        self.url: str = self.config['url']       # 问卷网址
        self.set: dict = self.config['wjx_set']   # 用户设置
        self.time: str = self.config['time']        # 报名开始时间

    def run(self):
        try:
            self.signUpActivity()
        except AssertionError as e:
            print(f"【错误】订单{self.oid}：{e}")
        else:
            # TODO: 更新wjx_result
            self.status = 500
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
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            time.sleep(starttime_stamp - time.time() + 1)
            page.goto(self.url)
            nodes = page.query_selector_all(".field.ui-field-contain")

            for node in nodes:

                # 跳过非必填项
                req_node = node.query_selector('.req')
                if not req_node:
                    continue

                # 解析题目和题型
                text_node = node.query_selector('.topichtml')
                text = text_node.inner_text()
                type_node = (node.query_selector_all('div:nth-child(2)'))[1]
                content = node.inner_html()

                # 填空题
                if 'ui-input-text' in content:
                    # 本地匹配
                    answer = None
                    for key in self.set.keys():
                        if key in text:
                            answer = self.set.get(key)
                    # 调用大模型获取答案
                    if not answer:
                        answer = '大模型'
                        pass
                    type_node.query_selector('input').fill(answer)

                # 单选/多选题
                elif 'ui-radio' in content or 'ui-checkbox' in content:
                    # 特判
                    if text == '性别' and self.set['性别'] in ['男', '女']:
                        page.get_by_text(self.set['性别']).click()
                        continue

                    # 解析选项
                    self.status = 911
                    raise AssertionError("正在开发...")
                    # options = ''
                    # option_nodes = type_node.query_selector_all('.label')
                    # for option in option_nodes:
                    #     option_text = option.inner_text()
                    #     options += option_text + '&'
                    # print("选项：", options)
                    # # 调用大模型获取答案
                    # resp = "大模型"
                    # answers = resp.split('&')
                    # print(answers)
                    # for ans in answers:
                    #     page.get_by_text(ans).click()

                else:
                    self.status = 910
                    raise AssertionError(f'遇到未知的问题类型：{type}')

            # 点击提交按钮
            page.query_selector('#ctlNext').click()
            time.sleep(10)
            browser.close()


if __name__ == '__main__':
    pass
    # task = Taskwjx()
    # task.execute()
