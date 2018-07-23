from flask import Flask
from flask_cors import CORS
from authark.infrastructure.config.context import Context
from authark.infrastructure.web.routes import set_routes


def create_app(context: Context) -> Flask:
    config = context.config
    registry = context.registry
    flask_config = config['flask']

    app = Flask(__name__)
    CORS(app)
    app.config.update(flask_config)

    set_routes(app, registry)

    return app
