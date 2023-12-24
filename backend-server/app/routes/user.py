import json
import time

from flask import Blueprint, request, session

from app.routes.filters import login_required
from app.models import db
from app.models.User import User
from app.models.Feedback import Feedback

user_bk = Blueprint('user', __name__, url_prefix='/user')

@login_required
@user_bk.post('/nick')
def nick():
    uid = session.get('uid')
    nickName = request.form.get("nick")
    length = len(nickName.encode('gbk'))
    if length < 2 or length > 18:
        return {"code": 1001}
    User.query.filter(User.uid==uid).update({"nick": nickName})
    db.session.commit()
    return {"code": 1000}


@login_required
@user_bk.post('/wjx_set')
def set_wjx():
    uid = session.get('uid')
    wjx_set = json.loads(request.form.get("wjx_set"))
    User.query.filter(User.uid==uid).update({"wjx_set": wjx_set})
    db.session.commit()
    return {"code": 1000}


@login_required
@user_bk.post('/feedback')
def feedback():
    uid = session.get('uid')
    ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    text = request.form.get("text")
    info = request.form.get("info")
    user = User.query.filter(User.uid==uid).first()
    if user:
        feed_back = Feedback(uid=uid, time=ctime, text=text, conn_info=info)
        db.session.add(feed_back)
        db.session.commit()
        return {"code": 1000}
    return {"code": 1001}


