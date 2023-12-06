import functools

from capp_config import create_app, SERVER_DOMAIN
from flask import request, render_template, redirect
import requests

app = create_app()


# 拦截器：身份验证
def login_required(func):
    @functools.wraps(func)
    def inner():
        sid = request.cookies.get("sid")  # 获取本地Cookie
        resp = requests.post(SERVER_DOMAIN + "/login", cookies={"sid": sid}, verify=False)
        if resp.json()["Code"] == 1000:
            return func()
        else:
            return redirect('/')

    return inner


# 全局模板变量
@app.context_processor
def inject_global_variables():
    return {'serverURL': SERVER_DOMAIN}


@app.route('/', methods=['GET', 'POST'])
def login():
    sid = request.cookies.get("sid")  # 获取本地Cookie
    resp = requests.post(SERVER_DOMAIN + "/login", cookies={"sid": sid}, verify=False)  # 后端请求验证
    if resp.json()["Code"] == 1000:
        return redirect("/user")
    return render_template("login.html")


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/user/')
@login_required
def user():
    return render_template('user.html')


@app.route('/wjx/order/')
@login_required
def wjx_order():
    return render_template('wjx_order.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, ssl_context=('./SSL/hmc.weactive.top.pem',
                                                   './SSL/hmc.weactive.top.key'))
