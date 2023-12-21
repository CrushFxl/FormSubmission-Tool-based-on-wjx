from flask import Blueprint, request, session

from app.routes.filters import login_required
from app.models import db
from app.models.User import User
from app.models.RechargeOrder import RechargeOrder

recharge_order_bk = Blueprint('order', __name__, url_prefix='/recharge')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


@recharge_order_bk.post('/commit')
@login_required
def commit():
    pass
