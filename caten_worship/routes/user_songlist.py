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

    songlist = SongList.query.filter_by(out_id=out_id).first()

    listowner = User.query.filter_by(id=songlist.user_id).first()

    sids = ""
    for i in range(len(songlist.songs_sid_list)):
        if i == 0:
            sids += songlist.songs_sid_list[i]
        else:
            sids += "+" + songlist.songs_sid_list[i]
    
    requestURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sids
    r = requests.get(requestURL)
    songs = json.loads(r.text)

    try:
        return render_template("songs/songlist.html", songs=songs, songlist=songlist, listowner=listowner), 200

    except TemplateNotFound:
        abort(404)

@songlist_edit_bp.route('/songlist/edit/<out_id>', methods=["GET", "PUT"])
@login_required
def edit(out_id):

    songlist = SongList.query.filter_by(out_id=out_id).first()

    if request.method == "GET":

        sids = ""
        for i in range(len(songlist.songs_sid_list)):
            if i == 0:
                sids += songlist.songs_sid_list[i]
            else:
                sids += "+" + songlist.songs_sid_list[i]
        
        requestURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sids
        r = requests.get(requestURL)
        songs = json.loads(r.text)

        return render_template("songs/songlist_edit.html", songlist=songlist, songs=songs)


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

        print("ajax put!")

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
            print("before append: ", songlist.songs_sid_list)
            tempList.append(song_sid)
            songlist.songs_amount += 1

            songlist.songs_sid_list = tempList

            songlist.update()

            print("after append: ", songlist.songs_sid_list)

            return jsonify({"success": True, "act": "append"})
    
    else:

        print("ajax failed.")
        return redirect("/")
