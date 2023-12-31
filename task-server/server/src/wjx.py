import json

class Task:
    def __init__(self, oid, config):
        self.oid = oid
        self.url = config['url']
        self.conf = config['wjx_set']
        self.run()

    def run(self):
        def _run():
            pass


# 业务测试用
if __name__ == '__main__':
    Task(123, {'url': 'https://www.wjx.cn/vm/evfoZuA.aspx',
               'wjx_set': {
                   '班级': '1',
                   '姓名': '22',
                   '学号': '',
                   '校区': '',
                   '性别': '',
                   '手机': '',
                   'strategy': 'ai'
               }})
