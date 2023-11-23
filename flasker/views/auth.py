from flask import Blueprint, render_template, request, abort

bp = Blueprint('auth', __name__, template_folder='/static/templates/')

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


@bp.route('/api.inv_code/', methods=['GET', 'POST'])
def invitation_code():
    if request.method == 'GET':
        return abort(403)

    # 检查手机号合法性
    name = request.form.get("name")
    if len(name) < 2:
        return "name_too_short", 400
    if len(name) > 20:
        return "name_too_long", 400

    # 检查密码合法性
    pwd = request.form.get("pwd")
    if len(pwd) < 6:
        return "pwd_too_short", 400
    if len(pwd) > 18:
        return "pwd_too_long", 400
    for i in pwd:
        if i not in pwd_regex:
            return "invalid_pwd", 400

    # 核销邀请码
    inv_code = request.form["inv_code"]
    if inv_code != "hmc":
        return "invalid_inv_code", 400

    return "ok", 200
