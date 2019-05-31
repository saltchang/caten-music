# routes/user_songlist.py

from flask import Blueprint, render_template, abort, flash, current_app
from jinja2 import TemplateNotFound

import requests
import json

user_songlist_bp = Blueprint("user_songlist_bp", __name__,
                    template_folder='templates')

song_list_by_id_bp = Blueprint("song_list_by_id_bp", __name__,
                    template_folder='templates')


@user_songlist_bp.route('/user/songlist')
def user_songlist():
    try:
        return render_template("songs/list_of_songlist.html"), 200

    except TemplateNotFound:
        abort(404)


@song_list_by_id_bp.route('/songlist/<list_id>')
def song_list_by_id(list_id):

    songlist = {'title': "測試歌單", 'owner': "光鹽", "updatetime": "2019-05-28", "is_private": True, "description": "這是一份敬拜讚美歌單，用作測試用途。這是一份敬拜讚美歌單，用作測試用途。這是一份敬拜讚美歌單，用作測試用途。這是一份敬拜讚美歌單，用作測試用途。這是一份敬拜讚美歌單，用作測試用途。"}
    song_description_list = [["這首歌是歡樂的，節奏快速。剩下的文字為測試用途。", "剩下的文字為測試用途。剩下的文字為測試用途。剩下的文字為測試用途。剩下的文字為測試用途。剩下的文字為測試用途。剩下的文字為測試用途。剩下的文字為測試用途。"], ["帶著感謝的心來唱。"], ["在神面前等候，帶著安靜的心，速度轉為慢。"], ["盼望而肯定的敬拜。反覆兩次後升Key結束。"]]
    dummy_list = ["1010066", "1007030", "2010013", "1011027"]

    sids = ""
    for i in range(len(dummy_list)):
        if i == 0:
            sids += dummy_list[i]
        else:
            sids += "+" + dummy_list[i]
    
    requestURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sids
    r = requests.get(requestURL)
    songs = json.loads(r.text)

    print(songs)

    try:
        return render_template("songs/songlist.html", songs=songs, song_amount=len(songs), songlist=songlist, song_description_list=song_description_list), 200

    except TemplateNotFound:
        abort(404)
