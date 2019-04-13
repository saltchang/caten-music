# routes/register.py

from flask import Blueprint, render_template, abort, request, redirect
from jinja2 import TemplateNotFound
from caten_worship.services import Validator, RegisterHandler, send_mail

register_bp = Blueprint("register_bp", __name__,
                        template_folder='templates')

@register_bp.route('/register', methods=["GET", "POST"])
def register():

    username = ""
    email = ""
    password = ""

    if request.method == "POST":
        username = request.values.get("username")
        email = request.values.get("email")
        password = request.values.get("password")

        if Validator().username(username_to_validate=username) == False:
            return render_template("403.html", error_message="使用者名稱已被註冊"), 403
        
        if Validator().email(email_to_validate=email) == False:
            return render_template("403.html", error_message="電子信箱已被註冊"), 403
        
        RegisterHandler().register_user(username=username, email=email, password=password)
        
        token = RegisterHandler().register_user.create_activate_token()

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
