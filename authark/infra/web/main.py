from typing import Dict
from flask import Flask
import authark.infra.web.routes as routes
from authark.infra.web.registry import Registry


def main(config: Dict[str, str] = None) -> Flask:

    app = Flask(__name__)
    registry = Registry()
    routes.set_routes(app, registry)

    return app
