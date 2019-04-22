# models/__init__.py

from .songs import songsDB
from .dbx import get_dbx
from .users import User
from .mails import mail
from .login_managers import login_manager


def init_app(app):
    mail.init_app(app)
    login_manager.init_app(app)
