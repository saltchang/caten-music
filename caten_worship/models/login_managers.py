# models/login_manager.py

from flask_login import LoginManager
from .users import User

login_manager = LoginManager()
login_manager.login_view = "login_bp.login"
login_manager.login_message = {"message": "請先登入", "category": "danger"}

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.filter_by(username=user_id).first()
    except:
        return None
