import json
import os
import requests
from server.config import config as env_conf
BACKEND_SERVER_DOMAIN = env_conf[os.getenv('ENV')].BACKEND_SERVER_DOMAIN

url = ("https://share.proxy.qg.net/get"
       "?key=ZNRADUCY&num=1"
       "&area=330100,330200,330300,330400,330500,330600,"
       "330700,330800,330900,331000,331100&isp=0"
       "&format=json&distinct=false")

def getIP():
    # 向后端服务器请求ip地址资源
    resp = requests.get(url=url)
    resp = resp.json()
    if resp['code'] != 'SUCCESS':
        raise "提取IP时出现错误：" + resp['code']
    print(f"获取到代理IP信息：{resp}")
    return resp['data'][0]['server']
