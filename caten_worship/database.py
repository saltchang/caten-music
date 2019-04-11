from caten_worship import app
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import SignatureExpired, BadSignature

db = SQLAlchemy(app)

# 密碼加密檢驗器
from caten_worship.password_handler import hash_generator, check_password

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    verification = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = hash_generator(password)

    def password_checker(self, password):
        """
        密碼驗證，驗證使用者輸入的密碼跟資料庫內的加密密碼是否相符
        :param password: 使用者輸入的密碼
        :return: True/False
        """
        return check_password(self.password_hash, password)

    def create_confirm_token(self, expires_in=3600):
        """
        利用itsdangerous來生成令牌，透過current_app來取得目前flask參數['SECRET_KEY']的值
        :param expiration: 有效時間，單位為秒
        :return: 回傳令牌，參數為該註冊用戶的id
        """
        s = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_id': self.id})
    
    def validate_confirm_token(self, token):
        """
        驗證回傳令牌是否正確，若正確則回傳True
        :param token:驗證令牌
        :return:回傳驗證是否正確，正確為True
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # 驗證
        except SignatureExpired:
            #  當時間超過的時候就會引發SignatureExpired錯誤
            return False
        except BadSignature:
            #  當驗證錯誤的時候就會引發BadSignature錯誤
            return False
        return data

    def __repr__(self):
        return 'User: %s, Email: %s' % (self.username, self.email)
