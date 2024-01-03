import os

from flask import Flask
from flask_cors import CORS

from .config import config
from server.api.database import db

ENV = os.getenv('ENV') or 'production'

app = Flask(__name__)
app.config.from_object(config[ENV])
CORS(app, supports_credentials=True)
db.init_app(app)