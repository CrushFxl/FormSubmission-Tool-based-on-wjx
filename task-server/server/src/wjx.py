import datetime
import json
import random
import re
import time
import requests
from bs4 import BeautifulSoup

from server.src import Task
from server import app
from server.api import proxy

header_get = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/avif,image/webp,image/apng,*/*;q=0.8,application/'
              'signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'www.wjx.cn',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

header_post = {
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '40',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT': '1',
    'Host': 'www.wjx.cn',
    'Origin': 'https://www.wjx.cn',
    'Pragma': 'no-cache',
    'Referer': '',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
}

# 构造的参数常量
submittype = 1
hlv = 1
jcn = 4
nw = 1
jwt = 3
jpm = 25

# 解密函数
def dataenc(jqnonce, ktimes):
    b = ktimes % 10
    if b == 0:
        b = 1
    c = []
    for char in jqnonce:
        e = ord(char) ^ b
        c.append(chr(e))
    return ''.join(c)


class Taskwjx(Task):
    def __init__(self, oid, type, config):
        super().__init__(oid, type, config)
        # 订单基本信息
        self.content = ''
        self.url = self.config['url']
        self.sttime = self.config['time']
        self.shortid = re.search(r"/vm/([a-zA-Z0-9]+)", self.url).group(1)
        self.strategy = self.config['wjx_set']['strategy']
        self.delay = self.config['wjx_set']['delay'] if 'delay' in self.config['wjx_set'] else 0
        self.wjx_set = []
        # 订单过程信息
        self.questions = {}
        self.postURL = ''
        self.submitdata = {'submitdata': ''}
        self.result = {}
        self.proxies = {}

    def run(self):
        try:
            self.initOrder()
            self.waitStart()
            self.getPage()
            self.getQuestions()
            self.matchAnswer()
            self.getPostURL()
            self.submit()
        except AssertionError as e:
            print(f"【{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}】"
                  f"【错误】订单{self.oid}：{e}")
        else:
            self.status = 500
        finally:
            self.close()

    def initOrder(self):
        print(f"【提示】开始运行订单{self.oid}问卷任务")
        wjx_set = [[k, v] for k, v in self.config['wjx_set'].items()]
        self.wjx_set = [i for i in wjx_set if (i[0] != "strategy") and (i[0] != "delay")]
        self.wjx_set.append(["联系方式", self.config['wjx_set']['手机']])
        self.wjx_set.append(["电话", self.config['wjx_set']['手机']])
        self.wjx_set.append(["是否", "是"])
        remark = self.config['remark']  # 备注
        if remark:
            for i in remark.split(';'):
                self.wjx_set.append(i.split(":"))

    def waitStart(self):
        starttime_stamp = time.mktime(time.strptime(self.sttime, "%Y-%m-%d %H:%M:%S"))
        nowtime_stamp = time.time()
        delay = starttime_stamp - nowtime_stamp - 30
        if delay < 0:
            self.status = 901
            raise AssertionError(f"活动已开始，无法执行")
        time.sleep(delay)
        self.proxies['https'] = proxy.getIP()  # 获取代理IP
        nowtime_stamp = time.time()
        time.sleep(starttime_stamp - nowtime_stamp + self.delay)

    def getPage(self):
        success = False
        for i in range(10):
            try:
                resp = requests.get(url=self.url, headers=header_get,
                                    timeout=3)
                assert 'divQuestion' in resp.text
                self.content = resp.text
                success = True
            except AssertionError:
                # print("未开始，尝试轮询...")
                time.sleep(1)
            except requests.exceptions.Timeout:
                print("【警告】连接超时")
            except requests.exceptions.ConnectionError as e:
                print("【警告】GET遇到连接问题：", e)
            if success:
                break
        if not success:
            self.status = 905
            raise AssertionError('请求获取网页时遇到问题')

    def getQuestions(self):
        soup = BeautifulSoup(self.content, 'lxml')
        ques = soup.find_all('div', class_='field ui-field-contain')
        for que in ques:
            prompt = que.find('div', class_='topichtml').get_text(strip=True)  # 题目
            qtype = que.find_all('div')[3]
            self.questions[prompt] = []
            if qtype['class'][0] == 'ui-input-text':  # 填空题
                pass
            elif qtype['class'][0] == 'ui-controlgroup':  # 选择题
                options = qtype.find_all('div', class_='label')
                for o in options:
                    self.questions[prompt].append(o.get_text())
            else:
                self.status = 910
                raise AssertionError("遇到未知的问题类型")

    def matchAnswer(self):
        num = 1     # 题号
        submitdata = ''
        for prompt, options in self.questions.items():
            if not options:  # 填空题
                for i in self.wjx_set:
                    if i[0] in prompt:
                        self.result['[填空题]' + prompt] = i[1]
                        submitdata += f'{num}${i[1]}}}'
                        break
                else:
                    self.result['[填空题]'+prompt] = '1'
                    submitdata += f'{num}${1}'

            else:  # 选择题
                cnt = 0
                submitdata += f'{num}$'
                for o in range(len(options)):
                    for i in self.wjx_set:
                        if i[0] in prompt and i[1] in options[o]:
                            cnt += 1
                            submitdata += f'{o+1}|'
                            self.result['[选择题]' + prompt] = options[o]
                            break
                if cnt == 0:
                    n = random.randint(1, len(options))
                    submitdata += f'{n}|'
                    self.result['[选择题]' + prompt] = options[n-1]
                submitdata = submitdata[:-1]+'}'  # 去除|分选项符，添加}分题符
            num += 1
        self.submitdata['submitdata'] = submitdata[:-1]      # 去除}分题符

    def getPostURL(self):
        t = int(time.time() * 1000)
        cst = t - 7
        shortid = self.shortid
        ktimes = random.randint(30, 200)
        jqnonce = re.search(r'.{8}-.{4}-.{4}-.{4}-.{12}', self.content).group()
        start_time = re.search(r'\d+?/\d+?/\d+?\s\d+?:\d{2}:\d{2}', self.content).group()
        rn = re.search(r'\d{9,10}(?=\.\d{8})', self.content).group()
        jqsign = dataenc(jqnonce, ktimes)
        self.postURL = f"https://www.wjx.cn/joinnew/processjq.ashx?" \
                       f"shortid={shortid}&starttime={start_time}&" \
                       f"cst={cst}&submittype={submittype}&ktimes={ktimes}&" \
                       f"hlv={hlv}&rn={rn}&jcn={jcn}&nw={nw}&jwt={jwt}&jpm={jpm}&" \
                       f"t={t}&jqnonce={jqnonce}&jqsign={jqsign}"

    def submit(self):
        header_post['Referer'] = self.url
        try:
            resp = requests.post(url=self.postURL, data=self.submitdata,
                                 headers=header_post, proxies=self.proxies)
        except requests.exceptions.ProxyError:
            self.status = 906
            raise AssertionError('无权或无效的代理IP')
        if '10〒' in resp.text:
            self.config['wjx_result'] = self.result
            print(f'【{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}】'
                  f'【提示】订单{self.oid}成功执行')
        elif '9〒' in resp.text:
            self.status = 907
            raise AssertionError('构造参数有误')
        elif '7〒' in resp.text or '22' in resp.text:
            self.status = 908
            raise AssertionError('提交问卷时出错')
        else:
            self.status = 909
            raise AssertionError('提交时发生未知错误')


if __name__ == '__main__':
    task = Taskwjx("123456", "wjx", json.dumps({
        "url": "https://www.wjx.cn/vm/Q4I1hPw.aspx# ",
        "wjx_set": {
            '班级': '魔法学院1年级3班',
            '姓名': '鲁迪乌斯',
            '学号': '0000000000',
            '手机': '0000000000'
        },
        "time": "2024-03-28 00:13:00",
        "remark": ""
    }))
    with app.app_context():
        task.execute()
