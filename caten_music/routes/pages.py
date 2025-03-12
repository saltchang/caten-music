# routes/pages.py

from flask import Blueprint, redirect

pages_bp = Blueprint('pages_bp', __name__, template_folder='templates')


@pages_bp.route('/pages/go/<goto>')
def go(goto):
    return redirect(goto)
