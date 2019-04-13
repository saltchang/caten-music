# routes/activate_account.py

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from caten_worship.helper import validate_activate_token
from caten_worship.services.registerServer import Activator

activate_account_bp = Blueprint("activate_account_bp", __name__,
                        template_folder='templates')

@activate_account_bp.route('/activate/account/check/<token>')
def activate_account(token):
    check_result = validate_activate_token(token)
    if check_result:
        Activator().activate_user(check_result)

        return "帳號啟動完成！謝謝！"

    else:
        return "錯誤：啟動連結已過期或錯誤。"
