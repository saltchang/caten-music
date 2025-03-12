# routes/register.py


from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from jinja2 import TemplateNotFound

from caten_music import helper, models

UserModel = models.UserModel
UserProfile = models.UserProfile
InvitationCode = models.InvitationCode
checkExist = helper.checkExist()

register_bp = Blueprint('register_bp', __name__, template_folder='templates')

ajax_validate_register_bp = Blueprint('ajax_validate_register_bp', __name__, template_folder='templates')


# 註冊
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    username = ''
    email = ''
    password = ''
    invitation_code = request.args.get('invitation_code', '')

    # method == "POST"
    if request.method == 'POST':
        # 取得註冊表單資料
        try:
            username = request.values.get('username')
            email = request.values.get('email')
            displayname = request.values.get('displayname')
            password = request.values.get('password')
            confirm_password = request.values.get('confirm_password')
            invitation_code = request.values.get('invitation_code')

            # 後端確認所有資料的格式，雖然前端已經過濾過
            check_result = helper.checkFormat(username, email, displayname, password)

        # 當有人故意送出奇怪的request
        except:
            return render_template('error/403.html', error_message="Don't Play With Me."), 400

        # 如果有欄位的資料錯誤，則回傳之前端
        for k, v in check_result.items():
            if not v:
                return render_template('error/403.html', error_message='Wrong ' + k.replace('_check', '')), 400

        # 如果兩次輸入的密碼不一樣
        if not password == confirm_password:
            return render_template('error/403.html', error_message='兩次輸入的密碼不一樣，請再試一次'), 400

        # 檢查 username 是否已註冊
        if checkExist.username(username=username):
            return render_template('error/403.html', error_message='使用者名稱已被註冊'), 400

        # 檢查 email 是否已註冊
        if checkExist.email(email=email):
            return render_template('error/403.html', error_message='電子信箱已被註冊'), 400

        is_valid, result = helper.validate_invitation_code(invitation_code)
        if not is_valid:
            return render_template('error/403.html', error_message=result), 400

        # 以上所有註冊資料確認完成，可以註冊帳號

        # 建立新的使用者物件
        new_user = UserModel()
        new_user.username = username
        new_user.email = email
        new_user.displayname = displayname
        new_user.password = password
        new_user.is_authenticated = True

        # 提交新使用者至資料庫中儲存
        new_user.save()

        # 產生新的使用者檔案並提交儲存
        new_user_profile = UserProfile()
        new_user_profile.user_id = new_user.id
        new_user_profile.save()

        if isinstance(result, InvitationCode):
            result.record_usage()

        try:
            return render_template('account/register_success.html', username=username), 201
        except TemplateNotFound:
            return redirect(url_for('home_bp.home')), 302

    # method = "GET"
    else:
        if current_user.is_authenticated:
            return redirect('/'), 302

        invitation_valid = False
        invitation_message = ''

        if invitation_code:
            is_valid, result = helper.validate_invitation_code(invitation_code)
            invitation_valid = is_valid
            if not is_valid:
                invitation_message = result

        try:
            return render_template(
                'account/register.html',
                invitation_code=invitation_code,
                invitation_valid=invitation_valid,
                invitation_message=invitation_message,
            ), 200

        except TemplateNotFound:
            abort(404)


# 前端 ajax 驗證即將註冊的表單資料是否重複 username 或 email
@ajax_validate_register_bp.route('/ajax/validate/register/<username_>/<email_>', methods=['POST'])
def ajax_validate_register(username_, email_):
    # 預設為不存在
    result = {'username': False, 'email': False}

    # 如果 username 已經存在，則回傳 True
    if checkExist.username(username=username_):
        result['username'] = True

    # 如果 email 已經存在，則回傳 True
    if checkExist.email(email=email_):
        result['email'] = True

    # 回傳 json
    return jsonify(result)
