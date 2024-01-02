from flask import Blueprint, render_template

from .filters import login_required

home_ft = Blueprint('home', __name__)


@home_ft.get('/home/')
@login_required
def home():
    return render_template("home.html")


@home_ft.get('/balance/')
@login_required
def balance():
    return render_template("balance.html")


@home_ft.get('/feedback/')
@login_required
def feedback():
    return render_template("feedback.html")


@home_ft.get('/config/')
@login_required
def config():
    return render_template("config.html")
