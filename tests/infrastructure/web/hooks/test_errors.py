from pytest import raises
from flask import Flask, abort
from authark.infrastructure.web.hooks.errors import register_error_handler


def test_handler_error():
    with raises(Exception):
        app = Flask(__name__)

        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 0

        @app.route("/test1")
        def test1():
            abort(400, "Test error handled")

        @app.route("/test2")
        def test2():
            raise Exception("Not HTTPException type")

        register_error_handler(app)

        response = app.test_client().get("/test1")

        assert response.status == '400 BAD REQUEST'

        response = app.test_client().get("/test2")
