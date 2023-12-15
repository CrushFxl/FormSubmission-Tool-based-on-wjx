class BaseConfig:
    HOST = "127.0.0.1"

class ProductionConfig(BaseConfig):
    PORT = 443
    SSL_CONTEXT = ('app/misc/hmc.weactive.top.key', 'app/misc/hmc.weactive.top.pem')
    CORS_DOMAIN = "https://hmc.weactive.top:12345"


class DevelopmentConfig(BaseConfig):
    PORT = 80
    DEBUG = True
    TESTING = True
    CORS_DOMAIN = "http://127.0.0.1:12345"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
