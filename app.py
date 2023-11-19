from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    # 登录校验
    user = request.form['user']
    pwd = request.form['pwd']
    return "提交完成"


@app.route('/main/')
def main():
    return render_template('main.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False, threading=True)
