import os
from datetime import timedelta


class BaseConfig:
    HOST = "0.0.0.0"
    PORT = 12345
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SSL_CONTEXT = ('app/misc/hmc.weactive.top.key', 'app/misc/hmc.weactive.top.pem')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    CORS_DOMAIN = "https://hmc.weactive.top"
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = 'WeactiveKey2023'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///C:\\Users\\24289\\Desktop\\weactive.db"
    SQLALCHEMY_ECHO = True
    CORS_DOMAIN = "http://127.0.0.1"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
