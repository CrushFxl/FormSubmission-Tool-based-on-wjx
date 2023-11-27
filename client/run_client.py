from settings import create_app
from flask import request, render_template, abort

app = create_app()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    # user = request.form.get("phone")
    # pwd = request.form.get("pwd")
    return abort(404)


@app.route('/register/')
def register():
    if request.method == 'GET':
        return render_template('register.html')


@app.route('/user/')
def user():
    return render_template('user.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
