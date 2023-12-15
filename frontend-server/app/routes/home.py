import os
import requests
from flask import Blueprint, request, redirect, render_template

from .filters import login_required
from app.config import config

home_ft = Blueprint('home', __name__)

URL = config[os.getenv('ENV') or 'production'].CORS_DOMAIN


@home_ft.get('/home/')
@login_required
def home():
    return render_template("home.html")
