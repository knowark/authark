from flask import Flask
from flask_cors import CORS
from authark.infrastructure.config.context import Context
from .api import create_api


def create_app(context: Context) -> Flask:
    app = Flask(__name__)
    CORS(app)

    config = context.config
    registry = context.registry

    app.config.update(config['flask'])

    create_api(app, registry)

    return app
