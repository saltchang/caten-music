# models/__init__.py

from .base import db
from .dbx import get_dbx
from .users import UserModel
from .users_profile import UserProfile
from .songlists import SongList
from .report import SongReport
from .mails import mail
from .login_managers import login_manager
from flask_migrate import Migrate


def init_app(app):
    mail.init_app(app)
    login_manager.init_app(app)
    db.create_all()
    db.init_app(app)
    migrate = Migrate(app, db)
