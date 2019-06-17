# routes/surfer.py

from flask import Blueprint, render_template, abort, request, redirect, current_app
from jinja2 import TemplateNotFound

from flask_login import login_required, current_user

import requests
import json

surfer_bp = Blueprint("surfer_bp", __name__,
                      template_folder='templates')

surf_bp = Blueprint("surf_bp", __name__,
                      template_folder='templates')

surf_one_bp = Blueprint("surf_one_bp", __name__,
                      template_folder='templates')


@surfer_bp.route('/surfer')
def surfer():

    if current_user.is_authenticated:
        current_user.login_update()

    try:
        return render_template("pages/surfer.html"), 200
    except TemplateNotFound:
        abort(404)

@surf_bp.route('/surf')
def surf():

    if current_user.is_authenticated:
        current_user.login_update()

    # 關鍵字：標題
    title = request.args.get("title")
    if title != "":
        return redirect("/"), 302

    # 關鍵字：集數
    c = request.args.get("c").replace(" ", "")
    if c == "":
        return redirect("/"), 302

    # 關鍵字：語言
    lang = request.args.get("lang").replace(" ", "")
    if lang == "":
        return redirect("/"), 302

    # 關鍵字：調性
    to = request.args.get("to")
    if to != "":
        return redirect("/"), 302

    # API 串接 搜尋

    requestURL = "https://church-music-api.herokuapp.com/api/songs/search?lang=" + lang + "&c=" + c + "&to=&title="

    r = requests.get(requestURL)

    if not r.status_code == 200:
        result = []
    else:
        result = json.loads(r.text)

    try:
        return render_template("songs/songs.html", songs=result, songs_num=len(result), mode="surf", c=c, lang=lang), r.status_code
    except TemplateNotFound:
        abort(404)

@surf_one_bp.route('/song/<sid>')
def surf_one(sid):

    if current_user.is_authenticated:
        current_user.login_update()

    # API

    requestURL = "https://church-music-api.herokuapp.com/api/songs/sid/" + sid

    r = requests.get(requestURL)

    if not r.status_code == 200:
        return redirect("/")
    else:
        result = json.loads(r.text)

    try:
        return render_template("songs/songs.html", songs=result, mode="one"), r.status_code
    except TemplateNotFound:
        abort(404)
