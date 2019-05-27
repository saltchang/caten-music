# routes/user_song_list.py

from flask import Blueprint, render_template, abort, flash, current_app
from jinja2 import TemplateNotFound

import requests
import json

user_song_list_bp = Blueprint("user_song_list_bp", __name__,
                    template_folder='templates')

song_list_by_id_bp = Blueprint("song_list_by_id_bp", __name__,
                    template_folder='templates')


@user_song_list_bp.route('/user/songlist')
def user_song_list():
    try:
        return render_template("songs/mysonglist.html"), 200

    except TemplateNotFound:
        abort(404)


@song_list_by_id_bp.route('/songlist/<list_id>')
def song_list_by_id(list_id):

    song_list= {'title': "測試歌單"}
    dummy_list = ["1010066", "1007032", "2010015", "1011032"]
    songs = []

    for sid in dummy_list:
        requestURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sid
        r = requests.get(requestURL)
        songs.append(json.loads(r.text))

    try:
        return render_template("songs/songlist_id.html", songs=songs, song_amount=len(songs), song_list=song_list), 200

    except TemplateNotFound:
        abort(404)
