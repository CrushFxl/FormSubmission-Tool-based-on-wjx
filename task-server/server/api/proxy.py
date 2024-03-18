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
    while True:
        resp = requests.get(url=url)
        resp = resp.json()
        if resp['code'] == 'SUCCESS':
            return resp['data'][0]['server']
        print("提取IP时出现错误，尝试重新提取")
