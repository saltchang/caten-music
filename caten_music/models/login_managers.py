# models/login_manager.py

from flask_login import LoginManager

from .users import UserModel

login_manager = LoginManager()
login_manager.login_view = 'login_bp.login'
login_manager.login_message = '請先登入以繼續，謝謝！'
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    try:
        return UserModel.query.filter_by(username=user_id).first()
    except:
        return None
