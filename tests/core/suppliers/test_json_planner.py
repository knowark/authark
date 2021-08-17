from pytest import raises
from authark.application.general import PlanSupplier
from authark.core.suppliers import JsonPlanSupplier
from authark.core.suppliers.plan.json_plan_supplier import schedulark


async def test_json_planner_instantiation() -> None:
    planner = JsonPlanSupplier('tasks.json')
    assert isinstance(planner, PlanSupplier)


async def test_json_planner_setup(monkeypatch) -> None:
    class MockPlanner:
        def __init__(self, queue):
            self.queue = queue

        async def setup(self):
            self._setup = True

    monkeypatch.setattr(schedulark, 'Planner', MockPlanner)

    planner = JsonPlanSupplier('tasks.json')

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

    planner = JsonPlanSupplier('tasks.json')

    await planner.defer('DailyJob', {'task': 'data'})

    assert planner.planner._job == 'DailyJob'
    assert planner.planner._payload == {'task': 'data'}
