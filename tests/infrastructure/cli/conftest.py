from pytest import fixture
from injectark import Injectark
from authark.infrastructure.core import (
    Config, TrialWebConfig, build_factory)
from authark.infrastructure.cli import Cli
from argparse import Namespace


@fixture
def cli() -> Cli:
    config = TrialWebConfig()
    strategy = config["strategy"]
    factory = build_factory(config)

    resolver = Injectark(strategy, factory)

    return Cli(config, resolver)


@fixture
def namespace() -> Namespace:
    return Namespace()
