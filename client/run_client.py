import functools

from settings import create_app, Config
from flask import request, render_template, redirect
import requests

serverURL = Config['server_ip']

app = create_app()


# 拦截器：身份验证
def login_required(func):
    @functools.wraps(func)
    def inner():
        sid = request.cookies.get("sid")  # 获取本地Cookie
        resp = requests.post(serverURL + "/login", cookies={"sid": sid})
        if resp.json()["Code"] == 1000:
            return func()
        else:
            return redirect('/')
    return inner


# 全局模板变量
@app.context_processor
def inject_global_variables():
    return {'serverURL': serverURL}


@app.route('/', methods=['GET', 'POST'])
def login():
    sid = request.cookies.get("sid")  # 获取本地Cookie
    resp = requests.post(serverURL + "/login", cookies={"sid": sid})  # 后端请求验证
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(Config['client_ip'].split(':')[-1]))
