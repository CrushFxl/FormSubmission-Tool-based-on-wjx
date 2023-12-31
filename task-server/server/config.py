class BaseConfig:
    CHERRYPY = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 10086,
        'engine.autoreload.on': False
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    CORS_DOMAIN = "https://api.weactive.top"
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(BaseConfig):
    CORS_DOMAIN = "http://127.0.0.1:15262"
    CHERRYPY = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 10086,
        'engine.autoreload.on': True,
    }
    DEBUG = True
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
