from flask import Flask
from flask_cors import CORS
from authark.infrastructure.config.config import Config
from authark.infrastructure.web.routes import set_routes


def create_app(config) -> Flask:
    registry = config['registry']
    flask_config = config['flask']

    app = Flask(__name__)
    CORS(app)
    app.config.update(flask_config)

    set_routes(app, registry)

    return app
