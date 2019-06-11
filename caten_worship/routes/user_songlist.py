# routes/user_songlist.py

from flask import Blueprint, render_template, abort, flash, current_app, request, redirect, jsonify, url_for
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

songlist_edit_bp = Blueprint("songlist_edit_bp", __name__,
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


@song_list_by_id_bp.route('/songlist/<out_id>')
@login_required
def song_list_by_id(out_id):

    songs = []

    songlist = SongList.query.filter_by(out_id=out_id).first()

    listowner = User.query.filter_by(id=songlist.user_id).first()

    if current_user.id != listowner.id:
        flash("您目前造訪的是一份私人歌單，<br>請先確認您擁有存取此歌單的權限，謝謝。", "danger")
        flash("純粹測試訊息", "warning")
        flash("恭喜您，已經成功更新歌單。", "success")
        flash("您的身份為訪客，請登入以獲得更多功能。<br>詳細情形請參閱會員功能。<br>或者造訪我們的管理員申請頁面，謝謝。", "primary")
        return redirect("/")

    sids = ""
    for i in range(len(songlist.songs_sid_list)):
        if i == 0:
            sids += songlist.songs_sid_list[i]
        else:
            sids += "+" + songlist.songs_sid_list[i]
    
    requestURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sids
    r = requests.get(requestURL)
    if r.status_code == 200:
        songs = json.loads(r.text)
    elif r.status_code == 404:
        songs = []

    old_description = songlist.description
    
    new_description = old_description.replace("\r\n", "<br>")
    print("new_description: ", new_description)

    try:
        return render_template("songs/songlist.html", songs=songs, songlist=songlist, listowner=listowner, new_description=new_description), 200

    except TemplateNotFound:
        abort(404)

@songlist_edit_bp.route('/songlist/edit/<out_id>', methods=["GET", "POST"])
@login_required
def edit(out_id):

    if request.method == "GET":

        songs = []

        songlist = SongList.query.filter_by(out_id=out_id).first()

        sids = ""
        for i in range(len(songlist.songs_sid_list)):
            if i == 0:
                sids += songlist.songs_sid_list[i]
            else:
                sids += "+" + songlist.songs_sid_list[i]
        
        requestURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sids
        r = requests.get(requestURL)
        if r.status_code == 200:
            songs = json.loads(r.text)
        elif r.status_code == 404:
            songs = []

        return render_template("songs/songlist_edit.html", songlist=songlist, songs=songs)
    
    elif request.method == "POST":

        songlist = SongList.query.filter_by(out_id=out_id).first()

        title = request.values.get("title")

        description = request.values.get("description")

        is_private = False

        if request.values.get("privacy") == "private":
            is_private = True
        
        is_archived = False

        if request.values.get("archive") == "archived":
            is_archived = True

        songs_amount = int(request.values.get("songs_amount"))

        songs_sid_list_new = []

        for index in range(songs_amount):
            songs_sid_list_new.append(request.values.get(str(index)))

        songlist.title = title
        songlist.description = description
        songlist.is_private = is_private
        songlist.is_archived = is_archived
        songlist.songs_amount = songs_amount

        songlist.songs_sid_list = None
        songlist.update()
        songlist.refresh()

        songlist.songs_sid_list = songs_sid_list_new

        songlist.update()

        return redirect(url_for("song_list_by_id_bp.song_list_by_id", out_id=out_id))


@add_songlist_bp.route('/songlist/add', methods=["GET", "POST"])
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

        songlist = SongList.query.filter_by(out_id=songlist_outid).first()

        tempList = songlist.songs_sid_list
        songlist.songs_sid_list = None
        songlist.update()
        songlist.refresh()

        
        if song_sid in tempList:
            tempList.remove(song_sid)
            songlist.songs_amount -= 1

            songlist.songs_sid_list = tempList

            songlist.update()

            return jsonify({"success": True, "act": "remove"})

        else:
            tempList.append(song_sid)
            songlist.songs_amount += 1

            songlist.songs_sid_list = tempList

            songlist.update()

            return jsonify({"success": True, "act": "append"})
    
    else:

        return redirect("/")
