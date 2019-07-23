# routes/pages.py

from flask import Blueprint, render_template, abort, flash, current_app, request, redirect, jsonify, url_for
from jinja2 import TemplateNotFound


pages_bp = Blueprint("pages_bp", __name__,
                    template_folder='templates')


@pages_bp.route('/pages/go/<goto>')
def go(goto):
    return redirect(goto)
