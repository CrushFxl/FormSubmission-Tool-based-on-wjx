# from flask import Blueprint, render_template, request, abort
#
# bp = Blueprint('auth', __name__)
#
#
# @bp.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template("login.html")
#
#     user = request.form.get("phone")
#     pwd = request.form.get("pwd")
#     return abort(404)
