from flask import Blueprint, request
bp = Blueprint('verify_inv_code', __name__)

pwd_regex = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.!@#%^&*()_+=-"
origin = {"Access-Control-Allow-Origin":"*"}


@bp.route('/verify_inv_code/', methods=['GET', 'POST'])
def verify_inv_code():
    # 检查手机号合法性
    name = request.form.get("name")
    if len(name) < 2:
        return "name_too_short", 400, origin
    if len(name) > 20:
        return "name_too_long", 400, origin

    # 检查密码合法性
    pwd = request.form.get("pwd")
    if len(pwd) < 6:
        return "pwd_too_short", 400, origin
    if len(pwd) > 18:
        return "pwd_too_long", 400, origin
    for i in pwd:
        if i not in pwd_regex:
            return "invalid_pwd", 400, origin

    # 核销邀请码
    inv_code = request.form["inv_code"]
    if inv_code != "hmc":
        return "invalid_inv_code", 400, origin

    return "ok", 200, origin
