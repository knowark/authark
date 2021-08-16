from pytest import fixture
from injectark import Injectark
from authark.core.common import config
from authark.factories import factory_builder
from authark.presenters.shell.jobs import NotifyJob


@fixture
def factory():
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)
    return factory


@fixture
def injector(factory):
    injector = Injectark(factory)
    return injector


def test_notify_job_instantiation(injector):
    job = NotifyJob(injector)

    assert job is not None


async def test_notify_job_call(injector):
    job = NotifyJob(injector)

    task = None
    result = await job(task)

    assert result == {}
