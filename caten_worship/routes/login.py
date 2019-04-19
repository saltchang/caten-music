# routes/login.py

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

login_bp = Blueprint("login_bp", __name__,
                    template_folder='templates')


@login_bp.route('/login')
def login():
    try:
        return render_template('login.html')

    except TemplateNotFound:
        abort(404)
