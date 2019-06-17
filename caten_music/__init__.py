# caten_music/__init__.py


import os

from flask import Flask

class CreateApp(object):

    def Main():

        global config

        config = os.environ.get("APP_SETTING")
        
        app = Flask(__name__)
        app.config.from_object(config)

        from . import models
        models.init_app(app)

        from . import routes
        routes.init_app(app)

        return app

    def Test():

        global config

        config = os.environ.get("TEST_SETTING")

        app = Flask(__name__)
        app.config.from_object(config)

        from . import models
        models.init_app(app)

        from . import routes
        routes.init_app(app)

        return app
