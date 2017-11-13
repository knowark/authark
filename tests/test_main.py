from pytest import fixture
from flask import Flask
from authark.main import app


def test_authark_main() -> None:
    assert isinstance(app, Flask)
