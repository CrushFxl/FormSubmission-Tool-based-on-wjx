import os
from flask import Blueprint, render_template

from .filters import login_required
from app.config import config

home_ft = Blueprint('home', __name__)

URL = config[os.getenv('ENV') or 'production'].CORS_DOMAIN


@home_ft.get('/home/')
@login_required
def home():
    return render_template("home.html")


@home_ft.get('/recharge/')
@login_required
def recharge():
    return render_template("recharge.html")


@home_ft.get('/feedback/')
@login_required
def feedback():
    return render_template("feedback.html")


@home_ft.get('/config/')
@login_required
def config():
    return render_template("config.html")
