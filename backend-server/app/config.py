import os
from datetime import timedelta


class BaseConfig:
    CHERRYPY = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 15262,
    }
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    FRONTEND_SERVER_DOMAIN = "https://hmc.weactive.top"
    TASK_SERVER_DOMAIN = "https://service.weactive.top"

    SESSION_COOKIE_DOMAIN = ".weactive.top"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(BaseConfig):
    FRONTEND_SERVER_DOMAIN = "http://127.0.0.1"
    TASK_SERVER_DOMAIN = "http://127.0.0.1:10086"

    SQLALCHEMY_DATABASE_URI = "sqlite:///C:/Users/24289/Desktop/weactive.db"
    CHERRYPY = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 15262,
        'engine.autoreload.on': True
    }
    SECRET_KEY = 'WeactiveKey2023'
    SQLALCHEMY_ECHO = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
