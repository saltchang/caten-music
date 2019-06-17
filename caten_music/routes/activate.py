# routes/activate_account.py

from flask import Blueprint, render_template, abort, request, jsonify, flash, redirect, url_for
from jinja2 import TemplateNotFound

from caten_music import helper
from caten_music import models
from caten_music import services

User = models.User

activate_account_bp = Blueprint("activate_account_bp", __name__,
                                template_folder='templates')

resend_activate_mail_bp = Blueprint("resend_activate_mail_bp", __name__,
                                template_folder='templates')

reset_password_bp = Blueprint("reset_password_bp", __name__,
                                template_folder='templates')

ajax_validate_email_bp = Blueprint("ajax_validate_email_bp", __name__,
                                template_folder='templates')


@activate_account_bp.route('/activate/account/check/<gate>/<token>')
def activate_account(gate, token):

    check_result = helper.checkActivateToken(token)

    if check_result:
        if gate == "account_activate":
            user = User.query.filter_by(id=check_result.get("user_id")).first()
            user.is_authenticated = True
            user.is_active = True
            user.save()

            return render_template("activation/active_success.html"), 200
        
        elif gate == "reset_password":
            return redirect(url_for("reset_password_bp.reset_password", step="setting", token=token))

        else:
            flash("錯誤的請求", "danger")
            return redirect("/")

    else:
        return render_template("activation/active_fail.html"), 400

@resend_activate_mail_bp.route('/activate/account/mail/resend', methods=["GET", "POST"])
def resend_activate_mail():

    if request.method == "POST":

        email = request.values.get("email")

        user = User.query.filter_by(email=email).first()

        if user:

            # 取得帳號名稱
            username = user.username

            # 確認 email 是否已經啟動過
            if user.is_authenticated:
                flash("此電子郵件已認證過，請再確認。", "danger")
                return redirect("/activate/account/mail/resend"), 302

            # 產生一個帳號啟動的 token
            token = user.create_activate_token()

            # 啟動 mail 服務
            # 寄出帳號啟動 email
            services.send_mail(sender='Sender@domain.com',
                               recipients=[email],
                               subject='Caten music 帳號註冊認證信',
                               template='activation/verifymail.html',
                               username=username,
                               mail_title="帳號註冊認證信",
                               message="歡迎你, 請點擊下面連結來啟用您的帳號",
                               link_msg="點此啟用您的帳號",
                               link_url=url_for('activate_account_bp.activate_account', gate="account_activate", token=token, _external=True),
                               token=token)

            return render_template("activation/after_register.html", msg_text="啟動信已成功寄出"), 200
        else:
            flash("電子郵件地址錯誤或尚未註冊", "danger")
            return redirect("/activate/account/mail/resend"), 302

    else:
        return render_template("activation/resend_mail.html"), 200


@reset_password_bp.route('/reset/password/<step>/<token>', methods=["GET", "POST"])
def reset_password(step, token):

    if step == "precheck":

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
                                subject='Caten music 密碼重設認證',
                                template='activation/verifymail.html',
                                username=username,
                                mail_title="密碼重設認證",
                                message="您好，請點擊下面連結以重設您的密碼",
                                link_url=url_for('activate_account_bp.activate_account', gate="reset_password", token=token, _external=True),
                                link_msg="點此重設",
                                token=token)

                flash("密碼重設信已經寄出，請前往您的信箱收取信件。", "primary")
                return redirect("/login")
            else:
                flash("電子郵件地址錯誤或尚未註冊", "danger")
                return redirect("/activate/account/mail/resend"), 302

        else:
            return render_template("activation/reset_password.html"), 200
    
    if step == "setting":

        if request.method == "POST":

            # 取得表單資料
            try:
                password = request.values.get("password")
                confirm_password = request.values.get("confirm_password")

                # 後端確認所有資料的格式，雖然前端已經過濾過
                check_result = helper.checkFormat(
                    "checkusername", "check@email.com", "checkdisplayname", password)

            # 當有人故意送出奇怪的request
            except:
                return render_template("error/403.html", error_message="Don't Play With Me."), 400

            # 如果有欄位的資料錯誤，則回傳之前端
            for k, v in check_result.items():
                if not v:
                    return render_template("error/403.html", error_message="Wrong " + k.replace("_check", "")), 400

            # 如果兩次輸入的密碼不一樣
            if not password == confirm_password:
                return render_template("error/403.html", error_message="兩次輸入的密碼不一樣，請再試一次"), 400


            # 以上資料確認完成，重設密碼

            check_result = helper.checkActivateToken(token)

            if check_result:

                user = User.query.filter_by(id=check_result.get("user_id")).first()

                user.reset_pw(password)

                user.update()

                flash("密碼重設成功，請重新登入", "success")
                return redirect("/login")
            
            else:

                flash("錯誤的驗證資訊", "danger")
                return redirect("/login")
        
        else:
            return render_template("account/form_reset_password.html", token=token), 200

    else:
        flash("請求錯誤", "danger")
        return redirect("/")

# 前端 ajax 驗證email
@ajax_validate_email_bp.route("/ajax/validate/email/<email_>", methods=["POST"])
def ajax_validate_email(email_):

    # 如果通過
    result = helper.checkExist().email(email_)

    # 回傳 json
    return jsonify(result)
