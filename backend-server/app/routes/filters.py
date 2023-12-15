import functools
from flask import session, redirect


def login_required(func):
    @functools.wraps(func)
    def inner():
        uid = session['uid']
        if uid:
            return func()
        else:
            return redirect('/login')
    return inner
