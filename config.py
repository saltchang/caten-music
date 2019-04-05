import os


class Config(object):
    class Default(object):
        DEBUG = False
        TESTING = False
        SECRET_KEY = os.environ.get("SECRET_KEY")
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_PG_URI")

    class Production(Default):
        ENV = "production"

    class Development(Default):
        ENV = "development"
        DEBUG = True

    class Testing(Default):
        ENV = "testing"
        TESTING = True
