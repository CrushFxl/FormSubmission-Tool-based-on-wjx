import threading
import time
from concurrent.futures import ThreadPoolExecutor

# import requests
# import os
#
# from server.config import config as env_conf
#
# ENV = os.getenv('ENV')
# TASK_SERVER_KEY = os.getenv('TASK_SERVER_KEY')
# BACKEND_SERVER_DOMAIN = env_conf[ENV].BACKEND_SERVER_DOMAIN


# class Task:
#     def __init__(self, oid, config):
#         self.oid = oid
#         self.url = config['url']
#         self.conf = config['wjx_set']
#         self.future = None
#         self.run()
#
#     def run(self):
#         def _run():
#             print("任务开始执行")
#             requests.post(url=BACKEND_SERVER_DOMAIN + '/service/accept',
#                           data={
#                               'key': TASK_SERVER_KEY,
#                               'oid': self.oid,
#                           })
#             time.sleep(30)
#             print("进行到一半了")
#             time.sleep(30)
#             print("任务完成")
#             requests.post(url=BACKEND_SERVER_DOMAIN + '/service/complete',
#                           data={
#                               'key': TASK_SERVER_KEY,
#                               'oid': self.oid,
#                           })
#         # self.future = executor.submit(_run)
#         pass

def wjx_task(oid, config):
    def _run():
        for i in range(120):
            print("订单号：", oid, "次序", i)
            time.sleep(1)

    thd = threading.Thread(target=_run)
    thd.start()
    print("结束")


# # 问卷星业务终端
# if __name__ == '__main__':
#
#     wjx_task_pool = ThreadPoolExecutor(max_workers=100)  # 初始化任务线程池

    # while True:
    #     cmd = input("> ")
    #     if cmd == 'stop':
    #         break
