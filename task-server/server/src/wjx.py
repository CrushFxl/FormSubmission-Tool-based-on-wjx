import os
import re

import requests
from flask import Blueprint, request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


wjx_bp = Blueprint('wjx', __name__, url_prefix='/wjx')


def isTaskValid():
    res = requests.get(wjx_url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    sttime = soup.find(id="divstarttime")
    if sttime is None:
        return {"code": 1005, "msg": "订单创建失败，此活动可能已开始报名或已结束报名，"
                                     "如果对此有疑问，请联系网站管理员。"}
    y, M, d, h = re.search(r"于(\d+)年(\d+)月(\d+)日 (\d+)点", sttime.text).groups()
    try:
        m = re.search(r"(\d+)分", sttime.text).groups()[0]
    except AttributeError:
        m = 0


@wjx_bp.get('/')
def task():
    # 身份验证（此key在后端服务器的环境变量中读入并携带）
    if request.form.get('key') != os.getenv('SECRET_KEY'):
        return {"code": 2000, "msg": "拒绝访问"}
    # 检查链接的有效性
    oid = request.form.get('oid')
    if not isTaskValid(oid):
        pass
    return {"code": 1000, "msg": "ok"}
