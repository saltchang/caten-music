# routes/user_song_list.py

from flask import Blueprint, render_template, abort, flash, current_app
from jinja2 import TemplateNotFound

user_song_list_bp = Blueprint("user_song_list_bp", __name__,
                    template_folder='templates')


@user_song_list_bp.route('/user/songlist')
def user_song_list():
    try:
        return render_template("songs/mysonglist.html"), 200

    except TemplateNotFound:
        abort(404)
