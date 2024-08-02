from flask import Blueprint, request, session

from app.models import to_json
from app.routes.filters import login_required
from app.models.BusinessOrder import BusinessOrder as bOrder
from app.models.RechargeOrder import RechargeOrder as rOrder
from app.models.User import User
from app.models.Message import Message
from app.models.Square import Square
from app.models import db

from app.routes.api.gpt_extract import getInfo
import hashlib
import re

query_bk = Blueprint('query', __name__, url_prefix='/query')


# 查询业务活动
@query_bk.get('/order')
@login_required
def query_order():
    uid = session.get('uid')
    oid = request.args['oid']
    order = bOrder.query.filter(bOrder.oid == oid, bOrder.uid == uid).first()
    if order:
        return {"code": 1000, "order": to_json(order)}
    return {"code": 1001}


# 查询业务活动列表
@query_bk.post('/orders')
@login_required
def query_orders():
    uid = session.get('uid')
    type = request.args['type']
    pn = int(request.args['pn'])
    sRange = [100, 999]
    if type == 'all':
        sRange = [100, 999]
    elif type == 'ing':
        sRange = [400, 499]
    elif type == 'done':
        sRange = [500, 599]
    pageObj = (bOrder.query.filter(bOrder.uid == uid,
                                   bOrder.status >= sRange[0],
                                   bOrder.status <= sRange[1])
               .order_by(bOrder.ctime.desc()).paginate(page=pn, per_page=10))
    ordersObj = pageObj.items
    orders = []
    for i in ordersObj:
        i = to_json(i)
        orders.append(i)
    # max_pn = pageObj.pages
    return {"code": 1000, "orders": orders}


# 查询用户主页信息
@query_bk.post('/user')
@login_required
def query_user():
    uid = session.get('uid')
    user = User.query.filter(User.uid == uid).first()
    ing = bOrder.query.filter(bOrder.uid == uid, bOrder.status == 400).count()
    done = bOrder.query.filter(bOrder.uid == uid, bOrder.status == 500).count()
    return {"code": 1000, "user": {"nick": user.nick,
                                   "balance": user.balance,
                                   "ing": ing,
                                   "done": done}}


# 查询充值活动支付状态
@query_bk.post('/recharge')
@login_required
def query_recharge_order():
    uid = session.get('uid')
    oid = request.form.get('oid')
    recharge_order = rOrder.query.filter(rOrder.oid == oid).first()
    if recharge_order.uid != str(uid):
        return {"code": 2000, "msg": '拒绝访问'}
    return {"code": 1000, "msg": 'ok', 'status': recharge_order.status}


# 查询是否存在未读消息
@query_bk.post('/msg_check')
@login_required
def query_msg_check():
    uid = session.get('uid')
    cnt = Message.query.filter(Message.uid == uid, Message.status == 0).count()
    if cnt:
        return {"code": 1000, "read": 0}
    else:
        return {"code": 1000, "read": 1}


# 获取所有消息
@query_bk.post('/msg_collect')
@login_required
def query_msg_collect():
    uid = session.get('uid')
    pageObj = (Message.query.filter(Message.uid == uid)
               .order_by(Message.date.desc())
               .paginate(page=1, per_page=10))
    msgObj = pageObj.items
    message = []
    for i in msgObj:
        i = to_json(i)
        message.append(i)

    msgs = Message.query.filter(Message.uid == uid)
    for m in msgs:
        m.status = 1  # 所有消息标记为已读
    db.session.commit()

    return {"code": 1000, "message": message}


def matchInfo(raw):
    dic = {}
    pattern = r'```([\s\S]*?)```'
    match = re.search(pattern, raw)
    raw2 = match.group(1)
    pattern2 = r'\"([\s\S]*?)\"'
    matches = re.findall(pattern2, raw2)
    for i in range(0, len(matches), 2):
        key = matches[i]
        value = matches[i + 1]
        dic[key] = value
    return dic


# 计算机设计大赛：GPT信息抽取
@query_bk.post('/extract')
@login_required
def query_extract():
    raw = request.form.get('raw')
    link = request.form.get('link')
    info = getInfo(raw)  # 抽取关键信息
    print('【信息抽取后】', info)
    dic = matchInfo(info)  # 清洗关键信息
    print('【数据清洗后】', dic)
    md5 = hashlib.md5()
    md5.update(raw.encode('utf-8'))
    aid = md5.hexdigest()  # 计算aid
    dic['aid'] = aid
    dic['raw'] = raw
    dic['link'] = link
    # 保存square
    square = Square(aid=aid, title=dic['title'], short=dic['short'],
                    stime=dic['stime'], atime=dic['atime'],
                    location=dic['location'], score=dic['score'],
                    raw=raw, link=link, limit=dic['limit'])
    db.session.add(square)
    db.session.commit()

    dic['code'] = 1000
    return dic


# 计算机设计大赛：square信息查询
@query_bk.post('/squares')
@login_required
def query_squares():
    # pn = int(request.args['pn'])
    pn = 1
    pageObj = (Square.query.filter(Square.n == 1)
               .order_by(Square.stime.desc()).paginate(page=pn, per_page=10))
    squareObj = pageObj.items
    squares = []
    for i in squareObj:
        i = to_json(i)
        squares.append(i)
    # max_pn = pageObj.pages
    print(squares)
    return {"code": 1000, "squares": squares}
