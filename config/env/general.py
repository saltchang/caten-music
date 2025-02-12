from decouple import config

APP_NAME: str = config("APP_NAME", default="Caten Music", cast=str)
