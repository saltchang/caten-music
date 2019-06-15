# routes/logout.py

from flask import Blueprint, render_template, abort, redirect
from jinja2 import TemplateNotFound
from flask_login import logout_user, current_user


logout_bp = Blueprint("logout_bp", __name__,
                    template_folder='templates')


@logout_bp.route("/logout", methods=["POST"])
def logout():
    try:
        if current_user.is_authenticated:
            current_user.login_update()

        logout_user()
        return redirect("/"), 302
    except:
        return redirect("/"), 302
