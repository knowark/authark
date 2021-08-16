import json
from typing import List
from injectark import Injectark
from unittest.mock import AsyncMock
from pytest import fixture, raises
from authark.core import config
from authark.factories import factory_builder
from authark.presenters.shell import Scheduler
from authark.presenters.shell.scheduler import schedulark


@fixture
def scheduler() -> Scheduler:
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    injector = Injectark(factory)

    return Scheduler(injector)


def test_scheduler_instantiation(scheduler):
    assert scheduler is not None
