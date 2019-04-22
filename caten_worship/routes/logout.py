# routes/logout.py

from flask import Blueprint, render_template, abort, redirect
from jinja2 import TemplateNotFound
from flask_login import logout_user


logout_bp = Blueprint("logout_bp", __name__,
                    template_folder='templates')


@logout_bp.route("/logout", methods=["POST"])
def logout():
    try:
        logout_user()
        return redirect("/")
    except:
        return redirect("/")
