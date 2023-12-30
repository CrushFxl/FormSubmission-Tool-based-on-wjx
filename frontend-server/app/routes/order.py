from flask import Blueprint, render_template

from .filters import login_required

order_ft = Blueprint('order', __name__)


@order_ft.get('/wjx_order_pre/')
@login_required
def wjx_order_pre():
    return render_template('wjx_order_pre.html')


@order_ft.get('/wjx_order_detail/')
@login_required
def wjx_order_detail():
    return render_template('wjx_order_detail.html')
