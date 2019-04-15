# routes/register.py

from flask import Blueprint, render_template, abort, request, redirect, jsonify
from jinja2 import TemplateNotFound
from caten_worship.services import Validator, RegisterHandler, send_mail

register_bp = Blueprint("register_bp", __name__,
                        template_folder='templates')

ajax_validate_register_bp = Blueprint("ajax_validate_register_bp", __name__,
                        template_folder='templates')

@register_bp.route('/register', methods=["GET", "POST"])
def register():

    username = ""
    email = ""
    password = ""

    if request.method == "POST":
        username = request.values.get("username")
        email = request.values.get("email")
        displayname = request.values.get("displayname")
        password = request.values.get("password")
        confirm_password = request.values.get("confirm-password")

        if not password == confirm_password:
            return render_template("403.html", error_message="輸入的確認密碼不正確，請再試一次")

        if Validator().username(username_to_validate=username) == False:
            return render_template("403.html", error_message="使用者名稱已被註冊"), 403
        
        if Validator().email(email_to_validate=email) == False:
            return render_template("403.html", error_message="電子信箱已被註冊"), 403
        
        token = RegisterHandler().register_user(username=username, email=email, password=password, displayname=displayname)

        send_mail(sender='Sender@domain.com',
                  recipients=[email],
                  subject='Caten Worship 帳號註冊認證信',
                  template='verifymail.html',
                  username=username,
                  token=token)
        try:
            return "請前往您註冊的信箱：" + email + " , 來啟用您的帳號，謝謝。", 201
        except TemplateNotFound:
            abort(404)
    
    else:
        return render_template("register.html")


@ajax_validate_register_bp.route("/ajax/validate/register/<username_>/<email_>")
def ajax_validate_register(username_, email_):

    result = []

    if Validator().username(username_to_validate=username_) == False:
        result.append({"username": False})
    else:
        result.append({"username": True})
    
    if Validator().email(email_to_validate=email_) == False:
        result.append({"email": False})
    else:
        result.append({"email": True})

    return jsonify(result)
