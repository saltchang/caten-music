# models/users.py

import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature

from caten_worship import helper

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTING"))
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    displayname = db.Column(db.String(16), nullable=False)
    activated = db.Column(db.Boolean, default=False)


    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")


    @password.setter
    def password(self, password):

        self.password_hash = helper.hash_generator(password)

        return self.password_hash


    def verify_password(self, password):
        """
        密碼驗證，驗證使用者輸入的密碼跟資料庫內的加密密碼是否相符
        :param password: 使用者輸入的密碼
        :return: True/False
        """
        return helper.check_password(password, self.password_hash)


    def create_activate_token(self, expires_in=3600*24):
        token_generator = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        id_ = self.id
        return token_generator.dumps({"user_id": id_})


    def save(self):

        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return 'User: %s, Email: %s' % (self.username, self.email)
