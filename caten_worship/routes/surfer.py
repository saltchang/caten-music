# routes/surfer.py

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

surfer_bp = Blueprint("surfer_bp", __name__,
                      template_folder='templates')


@surfer_bp.route('/surfer')
def surfer():

    try:
        return render_template("surfer.html")
    except TemplateNotFound:
        abort(404)
