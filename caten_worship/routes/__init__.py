# routes/__init__.py

from .home import home_bp
from .search import search_bp
from .surfer import surfer_bp
from .download_ppt import download_ppt_bp

def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(surfer_bp)
    app.register_blueprint(download_ppt_bp)
    return app