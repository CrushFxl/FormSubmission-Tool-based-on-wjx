from flask import Blueprint, render_template
from .filters import login_required


recharge_ft = Blueprint('recharge', __name__, url_prefix='/recharge')


@recharge_ft.get('/')
@login_required
def index():
    return render_template("recharge/index.html")


@recharge_ft.get('/result/')
@login_required
def result():
    return render_template("recharge/result.html")
