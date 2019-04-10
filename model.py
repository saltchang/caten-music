from catenWorship import app
from flask_sqlalchemy import SQLAlchemy

from config import Config

app.config.from_object(Config.Development)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(36), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

