# models/__init__.py

from .base import db
from .dbx import get_dbx
from .invitation import InvitationCode
from .login_managers import login_manager
from .mails import mail
from .report import SongReport
from .songlists import SongList
from .users import UserModel
from .users_profile import UserProfile


def init_app(app):
    mail.init_app(app)
    login_manager.init_app(app)

    db.init_app(app)
