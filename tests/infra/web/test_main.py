from pytest import fixture
from flask import Flask
from authark.infra.web.main import main


def test_web_main() -> None:
    app = main()
    assert isinstance(app, Flask)
