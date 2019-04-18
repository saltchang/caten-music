# routes/register.py

from flask import Blueprint, render_template, abort, request, redirect, jsonify, current_app
from jinja2 import TemplateNotFound
from caten_worship.services import Validator, send_mail
from caten_worship.helper import formatCheck
from caten_worship import models

register_bp = Blueprint("register_bp", __name__,
                        template_folder='templates')

ajax_validate_register_bp = Blueprint("ajax_validate_register_bp", __name__,
                        template_folder='templates')

list_all_users_bp = Blueprint("list_all_users_bp", __name__,
                        template_folder='templates')

@register_bp.route('/register', methods=["GET", "POST"])
def register():

    username = ""
    email = ""
    password = ""

    if request.method == "POST":
        try:
            username = request.values.get("username")
            email = request.values.get("email")
            displayname = request.values.get("displayname")
            password = request.values.get("password")
            confirm_password = request.values.get("confirm-password")

            check_result = formatCheck(username, email, displayname, password)
        
        except:
            return render_template("403.html", error_message="Don't Play With Me.")

        for k, v in check_result.items():
            if not v:
                return render_template("403.html", error_message="Wrong " + k.replace("_check", ""))

        if not password == confirm_password:
            return render_template("403.html", error_message="輸入的確認密碼不正確，請再試一次")

        if Validator().username(username_to_validate=username) == False:
            return render_template("403.html", error_message="使用者名稱已被註冊"), 403
        
        if Validator().email(email_to_validate=email) == False:
            return render_template("403.html", error_message="電子信箱已被註冊"), 403
        
        new_user = models.User(username=username, email=email, displayname=displayname, password=password)

        token = new_user.create_activate_token()

        new_user.save()

        send_mail(sender='Sender@domain.com',
                  recipients=[email],
                  subject='Caten Worship 帳號註冊認證信',
                  template='verifymail.html',
                  username=username,
                  token=token)
        try:
            return render_template("after_register.html"), 201
        except TemplateNotFound:
            abort(404)
    
    else:
        return render_template("register.html")


@ajax_validate_register_bp.route("/ajax/validate/register/<username_>/<email_>", methods=["POST"])
def ajax_validate_register(username_, email_):

    result = {"username": False, "email": False}

    if not Validator().username(username_to_validate=username_) == False:
        result["username"] = True
    
    if not Validator().email(email_to_validate=email_) == False:
        result["email"] = True

    return jsonify(result)

@list_all_users_bp.route("/list/all/users")
def list_all_users():
    all_users = models.User.query.all()

    return render_template("list_all_users.html", all_users=all_users)

