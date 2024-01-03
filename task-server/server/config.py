class BaseConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class ProductionConfig(BaseConfig):
    CHERRYPY = {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 10086,
    }
    BACKEND_SERVER_DOMAIN = "https://api.weactive.top"

class DevelopmentConfig(BaseConfig):
    CHERRYPY = {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 10086,
    }
    BACKEND_SERVER_DOMAIN = "http://127.0.0.1:15262"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
