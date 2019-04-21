# routes/login.py

from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound

from caten_worship import helper


login_bp = Blueprint("login_bp", __name__,
                    template_folder='templates')

ajax_validate_login_bp = Blueprint("ajax_validate_login_bp", __name__,
                                      template_folder='templates')


@login_bp.route("/login", methods=["GET" ,"POST"])
def login():

    if request.method == "POST":
        return "login-post"

    else:
        try:
            return render_template('login.html')

        except TemplateNotFound:
            abort(404)


# 前端 ajax 驗證即將登入的表單資料是否通過登入驗證
@ajax_validate_login_bp.route("/ajax/validate/login/<primary_type_>/<primary_>/<password_>", methods=["POST"])
def ajax_validate_login(primary_type_, primary_, password_):

    # 預設為不通過
    result = {"login_pass": False}

    # 如果通過
    if helper.checkLogin(primary_type=primary_type_, primary=primary_, password=password_):
        result["login_pass"] = True

    # 回傳 json
    return jsonify(result)
