# routes/register.py

from flask import Blueprint, render_template, abort, request, redirect, jsonify, current_app, flash
from jinja2 import TemplateNotFound
from flask_login import current_user

from caten_worship import services
from caten_worship import helper
from caten_worship import models

User = models.User
UserProfile = models.UserProfile
checkExist = helper.checkExist()

register_bp = Blueprint("register_bp", __name__,
                        template_folder='templates')

ajax_validate_register_bp = Blueprint("ajax_validate_register_bp", __name__,
                                      template_folder='templates')

show_user_bp = Blueprint("show_user_bp", __name__,
                              template_folder='templates')

# 註冊
@register_bp.route('/register', methods=["GET", "POST"])
def register():

    username = ""
    email = ""
    password = ""

    # method == "POST"
    if request.method == "POST":

        # 取得註冊表單資料
        try:
            username = request.values.get("username")
            email = request.values.get("email")
            displayname = request.values.get("displayname")
            password = request.values.get("password")
            confirm_password = request.values.get("confirm_password")

            # 後端確認所有資料的格式，雖然前端已經過濾過
            check_result = helper.checkFormat(
                username, email, displayname, password)

        # 當有人故意送出奇怪的request
        except:
            return render_template("403.html", error_message="Don't Play With Me.")

        # 如果有欄位的資料錯誤，則回傳之前端
        for k, v in check_result.items():
            if not v:
                return render_template("403.html", error_message="Wrong " + k.replace("_check", ""))

        # 如果兩次輸入的密碼不一樣
        if not password == confirm_password:
            return render_template("403.html", error_message="兩次輸入的密碼不一樣，請再試一次")

        # 檢查 username 是否已註冊
        if checkExist.username(username=username):
            return render_template("403.html", error_message="使用者名稱已被註冊"), 403

        # 檢查 email 是否已註冊
        if checkExist.email(email=email):
            return render_template("403.html", error_message="電子信箱已被註冊"), 403

        # 以上所有註冊資料確認完成，可以註冊帳號

        # 建立新的使用者物件
        new_user = User(
            username=username, email=email, displayname=displayname, password=password)

        # 提交新使用者至資料庫中儲存
        new_user.save()

        # 產生新的使用者檔案並提交儲存
        new_user_profile = UserProfile(user_id=new_user.id)
        new_user_profile.save()

        # 產生一個帳號啟動的 token
        token = new_user.create_activate_token()

        # 啟動 mail 服務
        # 寄出帳號啟動 email
        services.send_mail(sender='Sender@domain.com',
                           recipients=[email],
                           subject='Caten Worship 帳號註冊認證信',
                           template='verifymail.html',
                           username=username,
                           token=token)

        # 註冊完成，通知使用者收取認證信
        try:
            return render_template("after_register.html", msg_text="註冊資料已送出"), 201

        except TemplateNotFound:
            abort(404)

    # method = "GET"
    else:

        if current_user.is_authenticated:
            return redirect("/")

        # 產生註冊表單
        try:
            flash("register", "primary")
            return render_template("register.html")

        except TemplateNotFound:
            abort(404)


# 前端 ajax 驗證即將註冊的表單資料是否重複 username 或 email
@ajax_validate_register_bp.route("/ajax/validate/register/<username_>/<email_>", methods=["POST"])
def ajax_validate_register(username_, email_):

    # 預設為不存在
    result = {"username": False, "email": False}

    # 如果 username 已經存在，則回傳 True
    if checkExist.username(username=username_):
        result["username"] = True

    # 如果 email 已經存在，則回傳 True
    if checkExist.email(email=email_):
        result["email"] = True

    # 回傳 json
    return jsonify(result)


# 顯示目前所有使用者 (開發用途)
@show_user_bp.route("/show/user/<username>")
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template("show_user.html", user=user)
