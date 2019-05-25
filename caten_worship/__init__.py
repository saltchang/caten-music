# caten_worship/__init__.py


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



# def create_app(config_code):

#     global config

#     if config_code == "test":
#         config = os.environ.get("TEST_SETTING")
#     elif config_code == "app":
#         config = os.environ.get("APP_SETTING")
#     else:
#         print("Wrong Config Code.")
#         exit(1)

#     app = Flask(__name__)
#     app.config.from_object(config)

#     from . import models
#     models.init_app(app)

#     from . import routes
#     routes.init_app(app)

#     return app
