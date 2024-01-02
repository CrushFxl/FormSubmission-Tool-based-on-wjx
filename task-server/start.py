import threading
from threading import Thread
import cherrypy
import requests

from server import create_flask_app
from server.api import db

# def read_keyboard_input():
#     while True:
#         cmd = input("> ")
#
#         if cmd == 'stop':
#             break
#
#         resp = requests.post(url="http://127.0.0.1:10086", data=cmd+"sdsdfsdgsgzsfbsf$end;")
#         print("发送已完成，接收到的响应：", resp.text)


if __name__ == '__main__':

    # 启动数据库和服务器
    db.create_table()
    create_flask_app()
    cherrypy.engine.start()

    # # 监听键盘输入
    # read_keyboard_thd = Thread(target=read_keyboard_input)
    # read_keyboard_thd.start()
