from flask import Flask
import authark.infra.web.routes as routes


def main(config: dict = None) -> Flask:

    app = Flask(__name__)

    routes.set_routes(app)

    return app
