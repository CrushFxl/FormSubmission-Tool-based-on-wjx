from flask import Blueprint, request, redirect


index_ft = Blueprint('index', __name__)


@index_ft.get('/index/')
def re():
    return redirect('/')


@index_ft.get('/')
def index():
    session = request.cookies.get('session')
    if session:
        return redirect('/home')
    else:
        # 首页没做 暂时跳到登录页
        pass
        return redirect('/login')

