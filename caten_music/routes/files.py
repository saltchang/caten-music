# routes/download_ppt.py


from flask import Blueprint, flash, redirect, request
from flask_login import current_user, login_required

from caten_music import models

download_ppt_bp = Blueprint('download_ppt_bp', __name__, template_folder='templates')

download_sheet_bp = Blueprint('download_sheet_bp', __name__, template_folder='templates')

dbx = models.get_dbx()


@download_ppt_bp.route('/download/ppt/<sid>')
@login_required
def download_ppt(sid):
    if current_user.is_authenticated:
        current_user.login_update()

    return_url = request.args.get('next')

    try:
        result = dbx.files_get_temporary_link('/CatenMusic_Data/PPT/ppt_' + sid + '.ppt')
        return redirect(result.link), 302

    except Exception:
        pass

    try:
        result = dbx.files_get_temporary_link('/CatenMusic_Data/PPT/ppt_' + sid + '.pptx')
        return redirect(result.link), 302

    except Exception:
        flash('很抱歉，這首歌目前沒有投影片。', 'warning')
        return redirect(return_url)


@download_sheet_bp.route('/download/sheet/<sid>')
@login_required
def download_sheet(sid):
    if current_user.is_authenticated:
        current_user.login_update()

    return_url = request.args.get('next')

    try:
        result = dbx.files_get_temporary_link('/CatenMusic_Data/Sheet/' + sid + '.pdf')

        return redirect(result.link), 302

    except Exception as no_pdf_error:
        print(no_pdf_error)
        flash('很抱歉，這首歌目前沒有歌譜。', 'warning')
        return redirect(return_url)
