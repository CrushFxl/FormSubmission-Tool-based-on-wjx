import os
from flask import Blueprint, render_template

from .filters import login_required
from app.config import config

order_ft = Blueprint('order', __name__)

URL = config[os.getenv('ENV') or 'production'].CORS_DOMAIN


@order_ft.get('/wjx_order_pre/')
@login_required
def wjx_order_pre():
    return render_template('wjx_order_pre.html')


@order_ft.get('/wjx_order_detail/')
@login_required
def wjx_order_detail():
    return render_template('wjx_order_detail.html')
