# routes/download_ppt.py

from flask import Blueprint, redirect

from caten_worship import models

download_ppt_bp = Blueprint("download_ppt_bp", __name__,
                            template_folder='templates')

dbx = models.get_dbx()


@download_ppt_bp.route("/downloadppt/<id_>")
def download_ppt(id_):

    try:
        result = dbx.files_get_temporary_link(
            "/caten-worship/ppt/ppt_" + id_ + ".ppt")
        return redirect(result.link), 302

    except Exception as no_ppt_error:
        pass

    try:
        result = dbx.files_get_temporary_link(
            "/caten-worship/ppt/ppt_" + id_ + ".pptx")
        return redirect(result.link), 302

    except Exception as no_pptx_error:
        return "<h1>很抱歉，這首詩歌目前沒有投影片資料可供下載。<h1>", 404
