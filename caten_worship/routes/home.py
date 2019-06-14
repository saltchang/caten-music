# routes/home.py

from flask import Blueprint, render_template, abort, flash, current_app
from jinja2 import TemplateNotFound

from flask_login import current_user

home_bp = Blueprint("home_bp", __name__,
                    template_folder='templates')


@home_bp.route('/')
def seeHome():
    if not current_user.is_authenticated:
        flash("歡迎您！<br>建議先註冊您的帳號來使用完整功能哦！", "info")
    return render_template("pages/index.html"), 200
