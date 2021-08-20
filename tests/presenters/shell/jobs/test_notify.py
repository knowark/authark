from unittest.mock import MagicMock
from pytest import fixture
from aiohttp import ClientSession
from injectark import Injectark
from schedulark import Task
from authark.core.common import config
from authark.factories import factory_builder
from authark.presenters.shell.jobs import NotifyJob
from authark.presenters.shell.jobs import notify as notify_module


@fixture
def factory():
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)
    return factory


@fixture
def injector(factory):
    injector = Injectark(factory)
    injector.config['notification']['url'] = (
        'https://api.service.com/events')
    return injector


def test_notify_job_instantiation(injector):
    job = NotifyJob(injector)

    assert job is not None


async def test_notify_job_call(injector, monkeypatch):
    class MockClientSession(MagicMock(ClientSession)):
        async def close(self):
            pass
    monkeypatch.setattr(notify_module, 'ClientSession', MockClientSession)
    job = NotifyJob(injector)

    task = Task(payload={'meta': {}, 'data': [{'id': 'R001'}]})
    result = await job(task)

    assert result == {}
    session = job.session
    session.patch.assert_called_once()
    session.patch.assert_called_once_with(
        'https://api.service.com/events', json={
            'meta': {}, 'data': [{'id': 'R001'}]
        })
