# routes/logout.py

from flask import Blueprint, render_template, abort, redirect, flash, request
from jinja2 import TemplateNotFound
from flask_login import logout_user, current_user


logout_bp = Blueprint("logout_bp", __name__,
                    template_folder='templates')


@logout_bp.route("/logout", methods=["POST"])
def logout():
    try:
        if current_user.is_authenticated:
            current_user.login_update()
        
        return_url = request.values.get('return_url')

        logout_user()
        flash("您已成功登出", "primary")
        return redirect(return_url), 302
    except:
        flash("發生錯誤，請回報管理員", "danger")
        return redirect("/"), 302
