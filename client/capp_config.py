from flask import Flask
import os

DEV = int(os.getenv('WEACTIVE_SERVER_DEV'))
if DEV:
    SERVER_DOMAIN = "http://127.0.0.1:12345"
else:
    SERVER_DOMAIN = "https://hmc.weactive.top:12345"


def create_app():
    app = Flask(__name__)
    if DEV:
        app.config.from_mapping({"DEBUG": True, "TESTING": True})
    else:
        app.config.from_mapping({"DEBUG": False, "TESTING": True})
    return app
