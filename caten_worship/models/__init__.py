# models/__init__.py

from .songs import create_songs_db
from .dbxAPI import get_dbx
from .users import db, User

def init_app(app):
    db.init_app(app)
