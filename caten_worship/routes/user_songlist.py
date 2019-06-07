# routes/user_songlist.py

from flask import Blueprint, render_template, abort, flash, current_app, request, redirect, jsonify
from jinja2 import TemplateNotFound

from caten_worship.models import SongList, User, login_manager

from flask_login import login_required, current_user

import requests
import json

user_songlist_bp = Blueprint("user_songlist_bp", __name__,
                    template_folder='templates')

song_list_by_id_bp = Blueprint("song_list_by_id_bp", __name__,
                    template_folder='templates')

add_songlist_bp = Blueprint("add_songlist_bp", __name__,
                    template_folder='templates')

ajax_update_songlist_bp = Blueprint("ajax_update_songlist_bp", __name__,
                    template_folder='templates')


@user_songlist_bp.route('/user/songlist')
@login_required
def user_songlist():

    try:
        return render_template("songs/list_of_songlist.html"), 200

    except TemplateNotFound:
        abort(404)


@song_list_by_id_bp.route('/songlist/<list_id>')
@login_required
def song_list_by_id(list_id):

    # ForTest
    # songlist = {'title': "測試歌單", 'owner': "光鹽", "updatetime": "2019-05-28", "is_private": True, "description": "這是一份敬拜讚美歌單，用作測試用途。這是一份敬拜讚美歌單，用作測試用途。這是一份敬拜讚美歌單，用作測試用途。這是一份敬拜讚美歌單，用作測試用途。這是一份敬拜讚美歌單，用作測試用途。"}
    # song_description_list = [["這首歌是歡樂的，節奏快速。剩下的文字為測試用途。", "剩下的文字為測試用途。剩下的文字為測試用途。剩下的文字為測試用途。剩下的文字為測試用途。剩下的文字為測試用途。剩下的文字為測試用途。剩下的文字為測試用途。"], ["帶著感謝的心來唱。"], ["在神面前等候，帶著安靜的心，速度轉為慢。"], ["盼望而肯定的敬拜。反覆兩次後升Key結束。"]]
    # dummy_list = ["1010066", "1007030", "2010013", "1011027"]

    songlist = SongList.query.filter_by(out_id=list_id).first()

    sids = ""
    for i in range(len(songlist.songs_sid_list)):
        if i == 0:
            sids += songlist.songs_sid_list[i]
        else:
            sids += "+" + songlist.songs_sid_list[i]
    
    requestURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sids
    r = requests.get(requestURL)
    songs = json.loads(r.text)

    print(songs)

    try:
        return render_template("songs/songlist.html", songs=songs, song_amount=len(songs), songlist=songlist, song_description_list=songlist.songs_description_list), 200

    except TemplateNotFound:
        abort(404)


@add_songlist_bp.route('/add/songlist', methods=["GET", "POST"])
@login_required
def add_songlist():

    if request.method == "POST":
        posttype = request.values.get("posttype")
        title = request.values.get("title")
        privacy = request.values.get("privacy")

        is_private = False

        if posttype == "withsong":
            song_sid = request.values.get("song_sid")
            if privacy == "private":
                is_private = True
                
            new_songlist = SongList(title=title, user=current_user, songs_sid_list=[song_sid], songs_amount=1, is_private=is_private)

            new_songlist.flush()

            new_songlist.init()

            new_songlist.save()

            return render_template("songs/list_of_songlist.html"), 200

    else:
        try:
            return render_template("songs/list_of_songlist.html"), 200

        except TemplateNotFound:
            abort(404)


@ajax_update_songlist_bp.route('/ajax/update/songlist/<song_sid>/<songlist_outid>', methods=["PUT"])
@login_required
def update_songlist(song_sid, songlist_outid):
    
    if request.method == "PUT":

        print("ajax put!")

        songlist = SongList.query.filter_by(out_id=songlist_outid).first()
        
        if song_sid in songlist.songs_sid_list:
            songlist.songs_sid_list.remove(song_sid)
            songlist.songs_amount -= 1

            songlist.commit()

            return jsonify({"success": True, "act": "remove"})

        else:
            print(songlist.songs_sid_list)
            songlist.songs_sid_list = songlist.songs_sid_list.append(song_sid)
            print(songlist.songs_sid_list)
            songlist.songs_amount += 1

            songlist.commit()

            return jsonify({"success": True, "act": "append"})
    
    else:

        print("ajax failed.")
        return redirect("/")
