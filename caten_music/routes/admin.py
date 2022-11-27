# routes/admin.py

from flask import Blueprint, render_template, abort, flash, current_app, request, redirect, jsonify, url_for
from jinja2 import TemplateNotFound

from caten_music.models import User, login_manager
from caten_music import helper

from flask_login import login_required, current_user

import requests
import json
import os
import re

song_edit_bp = Blueprint("song_edit_bp", __name__,
                    template_folder='templates')

users_bp = Blueprint("users_bp", __name__,
                    template_folder='templates')

user_edit_bp = Blueprint("user_edit_bp", __name__,
                    template_folder='templates')

workspace_bp = Blueprint("workspace_bp", __name__,
                    template_folder="templates")

create_new_song_bp = Blueprint("create_new_song_bp", __name__,
                    template_folder="templates")

@workspace_bp.route('/admin/workspace', methods=['GET'])
@login_required
def workspace():

    # 更新使用者登入時間
    if current_user.is_authenticated:
        current_user.login_update()

    if not current_user.is_manager:
        flash("您並沒有權限。", "danger")
        return redirect("/")

    if request.method == "GET":
        return render_template("admin/workspace.html")

# 新增歌曲資料
@create_new_song_bp.route('/admin/create/song', methods=["GET", "POST"])
@login_required
def add():

    # 更新使用者登入時間
    if current_user.is_authenticated:
        current_user.login_update()
    
    # 確認使用者擁有管理員權限
    if not current_user.is_manager:
        flash("很抱歉，您並沒有新增歌曲的權限。", "danger")
        return redirect("/")

    if request.method == "GET":

        # Tonality Collection
        toColl = ["C", "Cm", "C#", "D", "Dm", "Db", "E", "Em", "Eb", "F",
                  "Fm", "F#m", "G", "Gm", "Gb", "A", "Am", "Ab", "B", "Bm", 
                  "Bb"]

        return render_template("admin/song_create.html", toColl=toColl)
    
    elif request.method == "POST":
        try:

            # 取得表單資料
            # 新增歌曲時，可以自訂語言、集數, 首數及 SID 為自動產生
            title = request.values.get("title")
            num_c = request.values.get("num_c")
            language = request.values.get("language")
            originalTitleOriginal = request.values.get("title_original")
            scripture = request.values.get("scripture")
            tonality = request.values.get("tonality")
            year = request.values.get("year")
            lyricist = request.values.get("lyricist")
            composer = request.values.get("composer")
            translator = request.values.get("translator")
            album = request.values.get("album")
            publisher = request.values.get("publisher")
            publisher_original = request.values.get("publisher_original")
            tempo = request.values.get("tempo")
            time_signature = request.values.get("time_signature")

            originLyrics = request.values.get("lyrics")

            title_original_old = originalTitleOriginal.split("/")
            title_original = []
            for title_o in title_original_old:
                title_o = title_o.strip()
                if len(title_o) > 0:
                    title_original.append(title_o)
            
            lyrics_old = originLyrics.split("\n")
            lyrics = []
            
            lyrics_len = len(lyrics_old)
            for i in range(lyrics_len):
                p = lyrics_old[i]
                if len(p) > 0:
                    p = p.strip()
                    p = p.replace("\n", "")
                    p = p.replace("\r", "")
                if len(p) > 0:
                    lyrics.append(p)

            mostAdminToken = os.environ.get("SONGS_DB_MOST_ADMIN_TOKEN")

            reqBase = helper.CHURCH_MUSIC_API_URL

            reqURL = reqBase + "/api/songs/search?lang=" + language + "&c=" + num_c + "&to=&title=&lyrics=&test=0"
            searchRes = json.loads(requests.get(reqURL).text)

            newNumI = 0
            if type(searchRes) == type([]):
                currentCollecAmount = len(searchRes)
                newNumI = currentCollecAmount + 1
            elif searchRes["Code"] == 1600:
                newNumI = 1

            newNumI = str(newNumI)

            newSong = {
                # "sid": sid, # SID 由後端產生
                "num_c": num_c,
                "num_i": newNumI,
                "title": title,
                "title_original": title_original,
                "scripture": scripture,
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
                "publisher_original": publisher_original,
                "language": language,
                "token" : mostAdminToken,
            }

            for key, value in newSong.items():
                if type(value) == type("string"):
                    newSong[key] = newSong[key].strip()

            newSong_json = json.dumps(newSong)

            print(newSong_json)

            postURL = helper.CHURCH_MUSIC_API_URL

            r_post = requests.post(postURL + "/api/songs", newSong_json)

            response = json.loads(r_post.text)
            # return r_post.text

            newSID = response["NewSID"]

            return_url = request.values.get("next")
            if not helper.is_safe_url(return_url):
                flash("不安全的連結", "danger")
                return abort(400)
            else:
                flash("成功新增歌曲 #" + newSID, "success")
                if not return_url:
                    return redirect("/")
                else:
                    return redirect(return_url)
        
        except Exception as error:
            print(error)
            flash("發生錯誤，請洽網站管理員。", "danger")
            return redirect("/")

@song_edit_bp.route('/admin/edit/song/<sid>', methods=["GET", "POST"])
@login_required
def edit(sid):

    # 更新使用者登入時間
    if current_user.is_authenticated:
        current_user.login_update()
    
    # 確認使用者擁有管理員權限
    if not current_user.is_manager:
        flash("很抱歉，您並沒有編輯歌曲的權限。", "danger")
        return redirect("/")

    # Get 歌曲資訊
    requestURL = helper.CHURCH_MUSIC_API_URL + "/api/songs/sid/" + sid

    r = requests.get(requestURL)

    if not r.status_code == 200:
        flash("錯誤的資訊", "danger")
        return redirect("/")
    else:
        result = json.loads(r.text)
        song = result[0]

    if request.method == "GET":

        return_url = request.values.get("next")
        
        # Tonality Collection
        toColl = ["C", "Cm", "C#", "D", "Dm", "Db", "E", "Em", "Eb", "F",
                  "Fm", "F#m", "G", "Gm", "Gb", "A", "Am", "Ab", "B", "Bm", 
                  "Bb"]
        
        # Get original titles
        song_title_original = ""
        len_title_o = len(song["title_original"])
        if len_title_o > 0:
            for i in range(len_title_o):
                if i == (len_title_o - 1):
                    song_title_original += song["title_original"][i]
                else:
                    song_title_original += song["title_original"][i] + " / "
        
        # Get lyrics
        song_lyrics = ""
        for p in song["lyrics"]:
            song_lyrics += p + "\n"

        return render_template("admin/song_edit.html", song=song, toColl=toColl, song_lyrics=song_lyrics, song_title_original=song_title_original, return_url=return_url)
    
    elif request.method == "POST":

        try:

            return_url = request.values.get("return_url")

            # 編輯歌曲時，不可更改語言、編號、sid
            # num_c = request.values.get("num_c")
            # num_i = request.values.get("num_i")
            # language = request.values.get("language")

            num_c = song["num_c"]
            num_i = song["num_i"]
            language = song["language"]

            # 取得表單資料
            title = request.values.get("title")
            originalTitleOriginal = request.values.get("title_original")
            scripture = request.values.get("scripture")
            tonality = request.values.get("tonality")
            year = request.values.get("year")
            lyricist = request.values.get("lyricist")
            composer = request.values.get("composer")
            translator = request.values.get("translator")
            album = request.values.get("album")
            publisher = request.values.get("publisher")
            publisher_original = request.values.get("publisher_original")
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

            title_original_old = originalTitleOriginal.split("/")
            title_original = []
            for title_o in title_original_old:
                title_o = title_o.strip()
                if len(title_o) > 0:
                    title_original.append(title_o)
            
            lyrics_old = originLyrics.split("\n")
            lyrics = []
            
            lyrics_len = len(lyrics_old)
            for i in range(lyrics_len):
                p = lyrics_old[i]
                if len(p) > 0:
                    p = p.strip()
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
                "title_original": title_original,
                "scripture": scripture,
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
                "publisher_original": publisher_original,
                "language": language,
                "token" : mostAdminToken,
            }

            newSong_json = json.dumps(newSong)

            putURL = helper.CHURCH_MUSIC_API_URL + "/api/songs/sid/" + sid

            r_put = requests.put(putURL, newSong_json)

            response = json.loads(r_put.text)
            # return r_put.text

            
            if not helper.is_safe_url(return_url):
                flash("不安全的連結", "danger")
                return abort(400)
            else:
                if not return_url:
                    return redirect("/")
                flash("成功編輯歌曲 #" + sid, "success")
                return redirect(return_url)
        
        except Exception as error:
            print(error)
            flash("發生錯誤，請洽網站管理員。", "danger")
            return redirect("/")

@users_bp.route('/admin/users', methods=['GET'])
@login_required
def users():

    # 更新使用者登入時間
    if current_user.is_authenticated:
        current_user.login_update()

    if not current_user.is_admin:
        flash("您並沒有管理員權限。", "danger")
        return redirect("/")

    if request.method == "GET":
        users = User.query.order_by(User.id).all()
        return render_template("admin/users.html", users=users)

@user_edit_bp.route('/admin/users/edit/<id_>', methods=['GET', 'POST'])
@login_required
def edit(id_):

    # 更新使用者登入時間
    if current_user.is_authenticated:
        current_user.login_update()

    if not current_user.is_admin:
        flash("您並沒有總管理員權限。", "danger")
        return redirect("/")
    
    if request.method == "GET":
        user = User.query.filter_by(id=id_).first()
        return render_template("admin/user_edit.html", user=user)

    elif request.method == "POST":
        
        try:
            user = User.query.filter_by(id=id_).first()
        except:
            flash("錯誤的使用者資訊", "danger")
        
        displayname = request.values.get("displayname")
        authority = request.values.get("authority")

        # 確認顯示名稱格式
        if re.fullmatch(r"^[\u4e00-\u9fa5_a-zA-Z0-9]{1,17}$", displayname):
            stringLen = 0

            for c in displayname:
                if re.fullmatch(r"^[\u4e00-\u9fa5]+$", c):
                    stringLen += 2
                else:
                    stringLen += 1

            if stringLen <= 16:
                user.displayname = displayname
            
            else:
                flash("編輯使用者顯示名稱時發生錯誤", "danger")
                return redirect("/")
        else:
            flash("編輯使用者顯示名稱時發生錯誤", "danger")
            return redirect("/")
        
        # 確認權限
        if authority == "admin":
            user.is_admin = True
            user.is_manager = True
        elif authority == "manager":
            user.is_admin = False
            user.is_manager = True
        elif authority == "normal":
            user.is_admin = False
            user.is_manager = False
        else:
            flash("編輯使用者權限時發生錯誤", "danger")
            return redirect("/")
        
        user.update()

        return redirect(url_for("users_bp.users"))
