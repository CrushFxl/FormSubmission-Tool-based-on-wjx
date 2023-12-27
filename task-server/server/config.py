class BaseConfig:
    HOST = "0.0.0.0"
    PORT = 15261
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    SSL_CONTEXT = ('server/misc/hmc.weactive.top.key', 'server/misc/hmc.weactive.top.pem')
    CORS_DOMAIN = "https://hmc.weactive.top"
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    CORS_DOMAIN = "http://127.0.0.1"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
