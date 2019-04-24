# caten_worship/__init__.py

# -*- coding: utf-8 -*-

from flask import Flask


def create_app(conf):
    from . import routes, models, db
    app = Flask(__name__)
    app.config.from_object(conf)
    routes.init_app(app)
    models.init_app(app)
    db.init_app(app)

    return app
