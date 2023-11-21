import re

from flask import Flask, render_template, request, abort

pwd_regex = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.!@#%^&*()_+=-"

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    # 登录校验
    user = request.form.get("phone")
    pwd = request.form.get("pwd")
    return abort(404)


@app.route('/register/')
def register():
    if request.method == 'GET':
        return render_template('register.html')


@app.route('/register/_invitation_code/', methods=['GET', 'POST'])
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8088, debug=False)
