from injectark import Injectark
from ..config import Config
from .api import create_api


def create_app(config: Config, resolver: Injectark):
    # app = Flask(__name__)
    # CORS(app)

    # app.config.update(config['flask'])
    # register_error_handler(app)
    # create_api(app, resolver)

    # return app
    return None
