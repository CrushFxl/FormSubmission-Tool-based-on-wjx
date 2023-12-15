import os
import requests
from flask import Blueprint, request, redirect, render_template, session

from .filters import login_required
from app.config import config

order_ft = Blueprint('order', __name__)

URL = config[os.getenv('ENV') or 'production'].CORS_DOMAIN


@order_ft.get('/wjx_order_pre/')
@login_required
def wjx_order():
    return render_template('wjx_order_pre.html')
