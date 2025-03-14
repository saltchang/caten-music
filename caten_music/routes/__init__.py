# routes/__init__.py

from flask import jsonify

from .activate import activate_account_bp, ajax_validate_email_bp, resend_activate_mail_bp, reset_password_bp
from .admin import create_new_song_bp, song_edit_bp, user_edit_bp, users_bp, workspace_bp
from .files import download_ppt_bp, download_sheet_bp
from .home import home_bp
from .invitation import invitation_admin_bp, invitation_api_bp
from .login import ajax_validate_login_bp, login_bp
from .logout import logout_bp
from .pages import pages_bp

# from .files import download_ppt_bp, download_sheet_bp, export_songs_data_bp
from .register import ajax_validate_register_bp, register_bp
from .report import report_bp
from .search import search_bp
from .songlist import (
    add_songlist_bp,
    ajax_update_songlist_bp,
    song_list_by_id_bp,
    songlist_delete_bp,
    songlist_edit_bp,
    user_songlist_bp,
)
from .surfer import surf_bp, surf_one_bp, surfer_bp


def init_app(app):
    @app.route('/api/health', methods=['GET'])
    def health_check():
        print('Health check request received')
        return jsonify({'status': 'OK'}), 200

    app.register_blueprint(home_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(surfer_bp)
    app.register_blueprint(surf_bp)
    app.register_blueprint(surf_one_bp)
    app.register_blueprint(download_ppt_bp)
    app.register_blueprint(download_sheet_bp)
    # app.register_blueprint(export_songs_data_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(activate_account_bp)
    app.register_blueprint(ajax_validate_register_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(ajax_validate_login_bp)
    app.register_blueprint(resend_activate_mail_bp)
    app.register_blueprint(reset_password_bp)
    app.register_blueprint(ajax_validate_email_bp)
    app.register_blueprint(user_songlist_bp)
    app.register_blueprint(song_list_by_id_bp)
    app.register_blueprint(add_songlist_bp)
    app.register_blueprint(songlist_edit_bp)
    app.register_blueprint(songlist_delete_bp)
    app.register_blueprint(ajax_update_songlist_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(song_edit_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(user_edit_bp)
    app.register_blueprint(create_new_song_bp)
    app.register_blueprint(workspace_bp)
    app.register_blueprint(invitation_admin_bp)
    app.register_blueprint(invitation_api_bp)
    app.register_blueprint(pages_bp)

    return app
