# routes/activate_account.py

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from caten_worship import helper
from caten_worship import models

User = models.User

activate_account_bp = Blueprint("activate_account_bp", __name__,
                                template_folder='templates')


@activate_account_bp.route('/activate/account/check/<token>')
def activate_account(token):

    check_result = helper.checkActivateToken(token)

    if check_result:
        user = User.query.filter_by(id=check_result.get("user_id")).first()
        user.activated = True
        user.save()

        return render_template("active_success.html")

    else:
        return render_template("active_fail.html")
