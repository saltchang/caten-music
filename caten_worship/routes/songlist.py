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

songlist_delete_bp = Blueprint("songlist_delete_bp", __name__,
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

@songlist_delete_bp.route("/songlist/delete/<out_id>", methods=["POST"])
@login_required
def delete(out_id):

    if request.method == "POST":

        songlist = SongList.query.filter_by(out_id=out_id).first()

        if not songlist:
            flash("錯誤的歌單資訊", "danger")
            return redirect("/")

        if songlist.user_id == current_user.id:
            songlist.kill_self()
            flash("已成功刪除歌單 #" + out_id, "success")
            return redirect(url_for("user_songlist_bp.user_songlist"))
    
        else:
            flash("想幹嘛？您沒有權限刪除此歌單。<br>請登入後再試一次，謝謝。", "danger")

    else:

        return redirect("/")


@song_list_by_id_bp.route('/songlist/<out_id>')
@login_required
def song_list_by_id(out_id):

    songs = []

    songlist = SongList.query.filter_by(out_id=out_id).first()

    if not songlist:
        flash("錯誤的歌單資訊", "danger")
        return redirect("/")

    listowner = User.query.filter_by(id=songlist.user_id).first()

    if current_user.id != listowner.id and songlist.is_private:
        flash("您目前造訪的是一份私人歌單，<br>請先確認您擁有存取此歌單的權限，謝謝。", "danger")
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

    songlist = SongList.query.filter_by(out_id=out_id).first()

    if not songlist:
        flash("錯誤的歌單資訊", "danger")
        return redirect("/")

    if current_user.id != songlist.user_id:
        flash("想幹嘛？你沒有權限編輯此歌單。<br>請登入後再試一次，謝謝。", "danger")
        return redirect("/")

    if request.method == "GET":

        songs = []

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

        if not songlist:
            return jsonify({"success": False, "message": "wrong out_id"})

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

        return jsonify({"success": False, "message": "wrong method"})
