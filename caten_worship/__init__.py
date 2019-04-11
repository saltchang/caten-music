# -*- coding: utf-8 -*-

# caten_worship/__init__.py

import os
from flask import Flask


def create_app():
    from . import routes, models
    app = Flask(__name__)
    app.config.from_object(os.environ.get("APP_SETTING"))
    routes.init_app(app)
    models.init_app(app)
    
    return app
