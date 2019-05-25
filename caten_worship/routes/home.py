# routes/home.py

from flask import Blueprint, render_template, abort, flash, current_app
from jinja2 import TemplateNotFound

home_bp = Blueprint("home_bp", __name__,
                    template_folder='templates')


@home_bp.route('/')
def seeHome():
    current_app.logger.info("Homepage visited!")
    try:
        return render_template("pages/index.html"), 200

    except TemplateNotFound:
        abort(404)
