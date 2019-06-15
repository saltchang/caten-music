# routes/login.py

from flask import Blueprint, render_template, abort, jsonify, request, redirect, url_for, flash
from jinja2 import TemplateNotFound
from flask_login import login_user, current_user

import datetime

from caten_worship import helper


login_bp = Blueprint("login_bp", __name__,
                    template_folder='templates')

ajax_validate_login_bp = Blueprint("ajax_validate_login_bp", __name__,
                                      template_folder='templates')


@login_bp.route("/login", methods=["GET" ,"POST"])
def login():

    # method == "POST"
    if request.method == "POST":

        # 取得登入表單資料
        try:
            primary = request.values.get("primary")
            password = request.values.get("password")
            next_url = request.values.get("next_url")

            # 後端確認所有資料的格式，雖然前端已經過濾過
            check_result = helper.checkLoginFormat(primary, password)

        # 當有人故意送出奇怪的request
        except Exception as error:
            print(error)
            return render_template("error/403.html", error_message="Don't Play With Me."), 400


        # 如果有欄位的資料錯誤，則回傳之前端
        if check_result["primary_check"] == "failed" or \
            not check_result["password_check"]:
            return render_template("error/403.html", error_message="Wrong login imformation."), 400

        user_to_login = helper.checkLogin(check_result["primary_check"], primary, password)

        if not user_to_login:
            return render_template("error/403.html", error_message="Wrong login imformation."), 400
        
        if not user_to_login.is_authenticated:
            return render_template("activation/account_not_activated.html"), 401
        
        if not user_to_login.is_active:
            flash("此帳號已被凍結，<br>請聯絡管理人員以協助處理，謝謝", "danger")
            return redirect("/")

        # 以上所有註冊資料確認完成，可以註冊帳號
        else:
            login_user(user_to_login, remember=True, duration=datetime.timedelta(weeks=2))

            user_to_login.login_update()

            if next_url == "None":
                flash(user_to_login.displayname + "，歡迎回來" , "success")
                return redirect("/"), 302

            if not helper.is_safe_url(next_url):
                return abort(400)
            else:
                print(next_url)
                flash(user_to_login.displayname + "，歡迎回來" , "success")
                return redirect(next_url), 302

    # method == "GET"
    else:

        if current_user.is_authenticated:
            return redirect("/"), 302

        try:
            return render_template('account/login.html', next_url=request.args.get("next")), 200

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
