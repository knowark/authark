from flask import Flask
from flask_cors import CORS
from authark.infra.config.config import Config
from authark.infra.web.routes import set_routes


def create_app(config) -> Flask:
    registry = config['registry']
    flask_config = config['flask']

    app = Flask(__name__)
    CORS(app)
    app.config.update(flask_config)

    set_routes(app, registry)

    return app
