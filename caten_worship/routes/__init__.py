# routes/__init__.py

from .home import home_bp
from .search import search_bp
from .surfer import surfer_bp, surf_bp, surf_one_bp
from .download_ppt import download_ppt_bp
from .register import register_bp, ajax_validate_register_bp, show_user_bp
from .activate_account import activate_account_bp, resend_activate_mail_bp, ajax_validate_email_bp
from .login import login_bp, ajax_validate_login_bp
from .logout import logout_bp
from .user_songlist import user_songlist_bp, song_list_by_id_bp, add_songlist_bp, songlist_edit_bp, ajax_update_songlist_bp


def init_app(app):

    app.register_blueprint(home_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(surfer_bp)
    app.register_blueprint(surf_bp)
    app.register_blueprint(surf_one_bp)
    app.register_blueprint(download_ppt_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(activate_account_bp)
    app.register_blueprint(ajax_validate_register_bp)
    app.register_blueprint(show_user_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(ajax_validate_login_bp)
    app.register_blueprint(resend_activate_mail_bp)
    app.register_blueprint(ajax_validate_email_bp)
    app.register_blueprint(user_songlist_bp)
    app.register_blueprint(song_list_by_id_bp)
    app.register_blueprint(add_songlist_bp)
    app.register_blueprint(songlist_edit_bp)
    app.register_blueprint(ajax_update_songlist_bp)

    return app
