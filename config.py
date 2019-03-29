class Config(object):
    class Default(object):
        DEBUG = False
        TESTING = False
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    class Production(Default):
        ENV = "production"

    class Development(Default):
        ENV = "development"
        DEBUG = True

    class Testing(Default):
        ENV = "testing"
        TESTING = True
