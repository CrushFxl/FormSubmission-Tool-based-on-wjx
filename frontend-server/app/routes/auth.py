from flask import Blueprint, render_template

auth_ft = Blueprint('auth', __name__)


@auth_ft.get('/login/')
def login():
    return render_template("login.html")


@auth_ft.route('/register/')
def register():
    return render_template("register.html")