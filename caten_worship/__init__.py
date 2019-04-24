# caten_worship/__init__.py


import os

from flask import Flask

config = os.environ.get("APP_SETTING")


def create_app():

    app = Flask(__name__)
    app.config.from_object(config)

    from . import models
    models.init_app(app)

    from . import routes
    routes.init_app(app)

    return app
