# caten_music/__init__.py

import os

from flask import Flask

config = ""

class DefaultConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    
    # flask-mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PROT = "587"
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class CreateApp:

    def Main():

        config = os.environ.get("APP_SETTING")
        
        app = Flask(__name__)

        app.config.from_object(DefaultConfig)
        
        if config == "Development":
            app.config.from_pyfile("./development.py")
        elif config == "Testing":
            app.config.from_pyfile("./testing.py")
        elif config == "Production":
            app.config.from_pyfile("./production.py")

        from . import models
        models.init_app(app)

        from . import routes
        routes.init_app(app)

        return app

    def Test():

        config = os.environ.get("TEST_SETTING")

        app = Flask(__name__)

        app.config.from_object(DefaultConfig)
        
        if config == "Development":
            app.config.from_pyfile("./development.py")
        elif config == "Testing":
            app.config.from_pyfile("./testing.py")
        elif config == "Production":
            app.config.from_pyfile("./production.py")

        from . import models
        models.init_app(app)

        from . import routes
        routes.init_app(app)

        return app
