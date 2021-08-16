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


async def test_scheduler_run(scheduler, monkeypatch):
    state = {}

    class MockScheduler:
        def __init__(self, queue):
            nonlocal state
            self.state = state
            self.state['queue'] = queue
            self.state['jobs'] = []

        def register(self, job):
            self.state['jobs'].append(job)

        async def time(self):
            self.state['time'] = True

        async def work(self):
            self.state['work'] = True


    monkeypatch.setattr(
        schedulark, "Scheduler", MockScheduler)

    options = {'time': True}
    await scheduler.run(options)

    assert state['time'] is True

    options = {'work': True}
    await scheduler.run(options)

    assert state['work'] is True
