# routes/home.py

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

home_bp = Blueprint("home_bp", __name__,
                    template_folder='templates')


@home_bp.route('/')
def seeHome():
    try:
        return render_template('index.html')

    except TemplateNotFound:
        abort(404)
