from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy(app)

# 密碼加密檢驗器
from password_handler import hash_generator, check_password

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

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

    def __repr__(self):
        return 'User: %s, Email: %s' % (self.username, self.email)
