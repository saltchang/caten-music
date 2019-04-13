# routes/search.py

from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from caten_worship import services, models

search_bp = Blueprint("search_bp", __name__,
                        template_folder='templates')

songsDB = models.create_songs_db()

@search_bp.route('/search')
def search():

    # 模式 = { "search": 搜尋, "surf": 瀏覽 }
    mode = request.args.get("m")

    # 範圍 = { "title": 依標題, "language": 依語言}
    scope = request.args.get("s")

    # 關鍵字
    keyword = request.args.get("q")

    if scope:
        if mode == "search":
            result = services.SearchCore(songsDB, scope, keyword)
        elif mode == "surf":
            result = services.SurfCore(songsDB, scope, keyword)
    else:
        return redirect("/")

    if not result:
        result = []
        c = ""
    else:
        c = result[1]["num_c"]
    
    try:
        return render_template("result.html", songs=result, songs_num=len(result), mode=mode, scope=scope, keyword=keyword, c=c)
    except TemplateNotFound:
        abort(404)
