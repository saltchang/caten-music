# models/users.py

import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from caten_worship import helper

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTING"))
db = SQLAlchemy(app)

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
        self.password_hash = helper.hash_generator(password)

    def password_checker(self, password):
        """
        密碼驗證，驗證使用者輸入的密碼跟資料庫內的加密密碼是否相符
        :param password: 使用者輸入的密碼
        :return: True/False
        """
        return helper.check_password(self.password_hash, password)

    def __repr__(self):
        return 'User: %s, Email: %s' % (self.username, self.email)
