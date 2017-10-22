from typing import Dict
from flask import Flask
import authark.infra.web.routes as routes


def main(config: Dict[str, str] = None) -> Flask:

    app = Flask(__name__)

    routes.set_routes(app)

    return app
