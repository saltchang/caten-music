# routes/admin.py

from flask import Blueprint, render_template, abort, flash, current_app, request, redirect, jsonify, url_for
from jinja2 import TemplateNotFound

from caten_music.models import User, login_manager
from caten_music import helper

from flask_login import login_required, current_user

import requests
import json
import os

song_edit_bp = Blueprint("song_edit_bp", __name__,
                    template_folder='templates')


@song_edit_bp.route('/song/edit/<sid>', methods=["GET", "POST"])
@login_required
def edit(sid):

    # 確認使用者登入
    if current_user.is_authenticated:
        current_user.login_update()
    
    # 確認使用者擁有管理員權限
    if not current_user.is_admin:
        flash("很抱歉，您並沒有編輯歌曲的權限。", "danger")
        return redirect("/")

    # Get 歌曲資訊
    requestURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sid

    r = requests.get(requestURL)

    if not r.status_code == 200:
        flash("錯誤的資訊", "danger")
        return redirect("/")
    else:
        result = json.loads(r.text)
        song = result[0]

    if request.method == "GET":
        # Tonality Collection
        toColl = ["C", "Cm", "C#", "D", "Dm", "Db", "E", "Em", "Eb", "F",
                  "Fm", "F#m", "G", "Gm", "Gb", "A", "Am", "Ab", "B", "Bm", 
                  "Bb"]
        
        # Get lyrics
        song_lyrics = ""
        for p in song["lyrics"]:
            song_lyrics += p + "\n"

        return render_template("admin/song_edit.html", song=song, toColl=toColl, song_lyrics=song_lyrics)
    
    elif request.method == "POST":
        try:

            # 前一頁的url
            return_url = request.values.get("next")

            # 編輯歌曲時，不可更改語言、編號、sid
            # num_c = request.values.get("num_c")
            # num_i = request.values.get("num_i")
            # language = request.values.get("language")

            num_c = song["num_c"]
            num_i = song["num_i"]
            language = song["language"]

            # 取得表單資料
            title = request.values.get("title")
            tonality = request.values.get("tonality")
            year = request.values.get("year")
            lyricist = request.values.get("lyricist")
            composer = request.values.get("composer")
            translator = request.values.get("translator")
            album = request.values.get("album")
            publisher = request.values.get("publisher")
            tempo = request.values.get("tempo")
            time_signature = request.values.get("time_signature")

            originLyrics = request.values.get("lyrics")

            # 編輯歌曲時，不可更改語言、編號、sid
            # sid = ""
            # if language == "Chinese":
            #     sid += "1"
            # else:
            #     sid += "2"

            # if len(num_c) < 2:
            #     sid += "00" + num_c
            # else:
            #     sid += "0" + num_c

            # if len(num_i) < 2:
            #     sid += "00" + num_i
            # else:
            #     sid += "0" + num_i
            
            lyrics_old = originLyrics.split("\n")
            lyrics = []
            
            lyrics_len = len(lyrics_old)
            for i in range(lyrics_len):
                p = lyrics_old[i]
                p = p.replace(" ", "")
                p = p.replace("\n", "")
                p = p.replace("\r", "")
                if len(p) > 0:
                    lyrics.append(p)
            mostAdminToken = os.environ.get("SONGS_DB_MOST_ADMIN_TOKEN")

            newSong = {
                "sid": sid,
                "num_c": num_c,
                "num_i": num_i,
                "title": title,
                "year": year,
                "lyricist": lyricist,
                "composer": composer,
                "translator": translator,
                "lyrics": lyrics,
                "tonality": tonality,
                "tempo": tempo,
                "time_signature": time_signature,
                "album": album,
                "publisher": publisher,
                "language": language,
                "token" : mostAdminToken,
            }

            newSong_json = json.dumps(newSong)

            putURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sid
            # putURL = "http://0.0.0.0:7700/api/songs/sid/" + sid

            r_put = requests.put(putURL, newSong_json)

            response = json.loads(r_put.text)
            # return r_put.text

            
            if not helper.is_safe_url(return_url):
                flash("不安全的連結", "danger")
                return abort(400)
            else:
                flash("成功編輯歌單 #" + sid, "success")
                return redirect(return_url)
        
        except Exception as error:
            print(error)
            flash("發生錯誤，請洽網站管理員。", "danger")
            return redirect("/")
