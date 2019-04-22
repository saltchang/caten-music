# routes/activate_account.py

from flask import Blueprint, render_template, abort, request, jsonify, flash, redirect
from jinja2 import TemplateNotFound

from caten_worship import helper
from caten_worship import models
from caten_worship import services

User = models.User

activate_account_bp = Blueprint("activate_account_bp", __name__,
                                template_folder='templates')

resend_activate_mail_bp = Blueprint("resend_activate_mail_bp", __name__,
                                template_folder='templates')

ajax_validate_email_bp = Blueprint("ajax_validate_email_bp", __name__,
                                template_folder='templates')


@activate_account_bp.route('/activate/account/check/<token>')
def activate_account(token):

    check_result = helper.checkActivateToken(token)

    if check_result:
        user = User.query.filter_by(id=check_result.get("user_id")).first()
        user.is_authenticated = True
        user.is_active = True
        user.save()

        return render_template("active_success.html")

    else:
        return render_template("active_fail.html")

@resend_activate_mail_bp.route('/activate/account/mail/resend', methods=["GET", "POST"])
def resend_activate_mail():

    if request.method == "POST":

        email = request.values.get("email")

        user = User.query.filter_by(email=email).first()

        if user:

            # 取得帳號名稱
            username = user.username

            # 產生一個帳號啟動的 token
            token = user.create_activate_token()

            # 啟動 mail 服務
            # 寄出帳號啟動 email
            services.send_mail(sender='Sender@domain.com',
                               recipients=[email],
                               subject='Caten Worship 帳號註冊認證信',
                               template='verifymail.html',
                               username=username,
                               token=token)

            return render_template("after_register.html", msg_text="啟動信已成功寄出")
        else:
            flash("Email錯誤或尚未註冊", "danger")
            return redirect("/activate/account/mail/resend")

    else:
        return render_template("resend_mail.html")

# 前端 ajax 驗證email
@ajax_validate_email_bp.route("/ajax/validate/email/<email_>", methods=["POST"])
def ajax_validate_email(email_):

    # 如果通過
    result = helper.checkExist().email(email_)

    # 回傳 json
    return jsonify(result)
