import re

from flask import Flask, render_template, request, abort

pwd_regex = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.!@#%^&*()_+=-"
phone_regex = ("^(13[0-9]|14[0|5|6|7|9]|15[0|1|2|3|5|6|7|8|9]|16[2|5|6|7]|17[0|1|2|"
               "3|5|6|7|8]|18[0-9]|19[1|3|5|6|7|8|9])\d{8}$")

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    # 登录校验
    user = request.form['user']
    pwd = request.form['pwd']
    print(request.method)
    return "提交完成"


@app.route('/register/')
def register():
    if request.method == 'GET':
        return render_template('register.html')


@app.route('/register/_invitation_code/', methods=['GET', 'POST'])
def invitation_code():
    if request.method == 'GET':
        return abort(403)

    # 检查手机号合法性
    phone = request.form["phone"]
    pattern = re.compile(phone_regex)
    if not pattern.search(phone):
        return "invalid_phone", 400

    # 检查密码合法性
    pwd = request.form["pwd"]
    if len(pwd) < 6:
        return "pwd_too_short", 400
    elif len(pwd) > 18:
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
