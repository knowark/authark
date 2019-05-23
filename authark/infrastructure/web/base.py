from flask import Flask
from flask_cors import CORS
from injectark import Injectark
from ..core import Config
from .hooks import register_error_handler
from .api import create_api


def create_app(config: Config, resolver: Injectark) -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.config.update(config['flask'])
    register_error_handler(app)
    create_api(app, resolver)

    return app
