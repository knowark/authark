from pytest import raises
from authark.application.general import PlanSupplier
from authark.integration.core.suppliers import JsonPlanSupplier, Job, Event
from authark.integration.core.suppliers.plan.json_plan_supplier import (
    schedulark)


class MockPlanner:
    def __init__(self, queue):
        self.queue = queue

    async def setup(self):
        self._setup = True

    async def defer(self, job, payload):
        self._job = job
        self._payload = payload


async def test_json_planner_instantiation() -> None:
    planner = JsonPlanSupplier('tasks.json')
    assert isinstance(planner, PlanSupplier)


async def test_json_planner_setup(monkeypatch) -> None:
    monkeypatch.setattr(schedulark, 'Planner', MockPlanner)
    planner = JsonPlanSupplier('tasks.json')

    await planner.setup()

    assert planner.planner._setup is True


async def test_json_planner_defer(monkeypatch) -> None:
    monkeypatch.setattr(schedulark, 'Planner', MockPlanner)
    planner = JsonPlanSupplier('tasks.json')

    await planner.defer('DailyJob', {'task': 'data'})

    assert planner.planner._job == 'DailyJob'
    assert planner.planner._payload == {'task': 'data'}


async def test_json_planner_perform(monkeypatch) -> None:
    monkeypatch.setattr(schedulark, 'Planner', MockPlanner)
    planner = JsonPlanSupplier('tasks.json')
    class MigrationJob(Job):
        """Data Migration Job"""

    await planner.perform(MigrationJob(**{'job': 'data'}))

    assert planner.planner._job == 'MigrationJob'
    assert planner.planner._payload == {'meta': {}, 'data': {'job': 'data'}}


async def test_json_planner_notify(monkeypatch) -> None:
    monkeypatch.setattr(schedulark, 'Planner', MockPlanner)
    planner = JsonPlanSupplier('tasks.json')
    class ModelUpdated(Event):
        """Model Updated Event"""

    await planner.notify(ModelUpdated(**{'event': 'data'}))

    assert planner.planner._job == 'NotifyJob'
    assert planner.planner._payload == {
        'meta': {
            'event': {
                'name': 'ModelUpdated'
            }
        },
        'data': {'event': 'data'}
    }
