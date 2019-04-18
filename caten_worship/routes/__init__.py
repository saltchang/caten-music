# routes/__init__.py

from .home import home_bp
from .search import search_bp
from .surfer import surfer_bp
from .download_ppt import download_ppt_bp
from .register import register_bp, ajax_validate_register_bp, list_all_users_bp
from .activate_account import activate_account_bp


def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(surfer_bp)
    app.register_blueprint(download_ppt_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(activate_account_bp)
    app.register_blueprint(ajax_validate_register_bp)
    app.register_blueprint(list_all_users_bp)
    return app
