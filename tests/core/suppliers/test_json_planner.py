from pytest import raises
from authark.application.general import Planner
from authark.core.suppliers import JsonPlanner
from authark.core.suppliers.json_planner import schedulark


async def test_json_planner_instantiation() -> None:
    planner = JsonPlanner('tasks.json')
    assert isinstance(planner, Planner)


async def test_json_planner_setup(monkeypatch) -> None:
    class MockPlanner:
        def __init__(self, queue):
            self.queue = queue

        async def setup(self):
            self._setup = True

    monkeypatch.setattr(schedulark, 'Planner', MockPlanner)

    planner = JsonPlanner('tasks.json')

    await planner.setup()

    assert planner.planner._setup is True


async def test_json_planner_defer(monkeypatch) -> None:
    class MockPlanner:
        def __init__(self, queue):
            self.queue = queue

        async def defer(self, job, payload):
            self._job = job
            self._payload = payload

    monkeypatch.setattr(schedulark, 'Planner', MockPlanner)

    planner = JsonPlanner('tasks.json')

    await planner.defer('DailyJob', {'task': 'data'})

    assert planner.planner._job == 'DailyJob'
    assert planner.planner._payload == {'task': 'data'}
