import os
import requests

from server.config import config

BACKEND_SERVER_DOMAIN = config[os.getenv('ENV')].BACKEND_SERVER_DOMAIN

def update(oid, status):
    resp = requests.post(url=BACKEND_SERVER_DOMAIN + '/update',
                         data={'oid': oid, 'status': status})
    code = resp.json().get('code')
    if code != 1000:
        print("【警告】向后端服务器发送更新请求时失败，"
              f"订单号：{oid}，订单状态：{status}，返回状态码：{code}")
