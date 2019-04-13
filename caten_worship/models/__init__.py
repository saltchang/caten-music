# models/__init__.py

from .songs import songsDB
from .dbxAPI import get_dbx
from .users import db, User
from .mails import mail

def init_app(app):
    db.create_all()
    db.init_app(app)
    mail.init_app(app)
