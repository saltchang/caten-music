# caten_music/__init__.py

import os

from dotenv import load_dotenv
from flask import Flask

config = ''


class DefaultConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PROT = '587'
    MAIL_USE_TLS = True


class CreateApp:
    def main(self):
        load_dotenv()

        config = os.environ.get('APP_SETTING')

        app = Flask(__name__)

        with app.app_context():
            app.config.from_object(DefaultConfig)

            app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
            app.config['CONTACT_EMAIL'] = os.environ.get('CONTACT_EMAIL')

            if config == 'Development':
                app.config.from_pyfile('./development.py')
            elif config == 'Testing':
                app.config.from_pyfile('./testing.py')
            elif config == 'Production':
                app.config.from_pyfile('./production.py')

            if not app.config.get('SQLALCHEMY_DATABASE_URI'):
                raise RuntimeError('DATABASE_URL environment variable is not set')

            from . import models

            models.init_app(app)

            from . import routes

            routes.init_app(app)

            from . import helper

            helper.handleAPISchedule()

            @app.context_processor
            def inject_contact_email():
                return dict(contact_email=app.config['CONTACT_EMAIL'])

            return app

    def test(self):
        load_dotenv()

        config = os.environ.get('TEST_SETTING')

        app = Flask(__name__)

        with app.app_context():
            app.config.from_object(DefaultConfig)

            app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

            if config == 'Development':
                app.config.from_pyfile('./development.py')
            elif config == 'Testing':
                app.config.from_pyfile('./testing.py')
            elif config == 'Production':
                app.config.from_pyfile('./production.py')

            from . import models

            models.init_app(app)

            from . import routes

            routes.init_app(app)

            return app
