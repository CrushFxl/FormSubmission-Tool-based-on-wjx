from flask import Blueprint, render_template, request, abort

bp = Blueprint('auth', __name__, template_folder='../static/templates/')

pwd_regex = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.!@#%^&*()_+=-"


@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    # 登录校验
    user = request.form.get("phone")
    pwd = request.form.get("pwd")
    return abort(404)


@bp.route('/register/')
def register():
    if request.method == 'GET':
        return render_template('register.html')
