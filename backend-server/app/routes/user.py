import json
from flask import Blueprint, request, session

from app.routes.filters import login_required
from app.models import db
from app.models.User import User

user_bk = Blueprint('user', __name__, url_prefix='/user')


@login_required
@user_bk.post('/wjx_set')
def set_wjx():
    uid = session.get('uid')
    wjx_set = json.loads(request.form.get("wjx_set"))
    User.query.filter(User.uid==uid).update({"wjx_set": wjx_set})
    db.session.commit()
    return {"code": 1000}
