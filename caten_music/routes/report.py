# routes/report.py

from flask import Blueprint, render_template, abort, jsonify, request, redirect, url_for, flash
from jinja2 import TemplateNotFound
from flask_login import login_user, current_user, login_required

import datetime
import requests
import json

from caten_music import helper

report_bp = Blueprint("report_bp", __name__,
                    template_folder='templates')


@report_bp.route("/report/song/<sid>", methods=["GET" ,"POST"])
@login_required
def report_song(sid):

    requestURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sid

    r = requests.get(requestURL)

    if not r.status_code == 200:
        return redirect("/")
    else:
        result = json.loads(r.text)
        song = result[0]

    # method == "POST"
    if request.method == "POST":

        # 取得登入表單資料
        try:
            report_content = request.values.get("report_content")
            next_url = request.values.get("next_url")

            if len(report_content) < 5:
                next_url = next_url.replace('/', '%2F').replace('?', '%3F').replace('=', '%3D').replace('&', '%26')
                flash("回報的內容至少需要5個字。", "danger")
                return redirect(url_for("report_bp.report_song", sid=sid) + '?next=' + next_url)

        # 當有人故意送出奇怪的request
        except Exception as error:
            print(error)
            return render_template("error/403.html", error_message="Don't Play With Me."), 403
        
        print("report_content: ", report_content)
        print("report_user: ", current_user.id)

        if next_url == "None":
            flash("已順利回報歌曲問題 #" + sid, "success")
            return redirect("/"), 302

        if not helper.is_safe_url(next_url):
            return abort(400)
        else:
            flash("已順利回報歌曲問題 #" + sid, "success")
            return redirect(next_url), 302

    # method == "GET"
    else:
        try:
            return render_template('report/report_song.html', next_url=request.args.get("next"), song=song), 200

        except TemplateNotFound:
            abort(404)
