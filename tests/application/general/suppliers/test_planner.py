from pytest import raises
from authark.application.general import Planner, MemoryPlanner


def test_planner_methods() -> None:
    methods = Planner.__abstractmethods__  # type: ignore
    assert 'setup' in methods
    assert 'defer' in methods


async def test_memory_planner_setup() -> None:
    planner = MemoryPlanner()

    await planner.setup()

    assert planner._setup_calls == [True]


async def test_memory_planner_defer() -> None:
    planner = MemoryPlanner()

    await planner.defer('DailyJob', {'task': 'data'})

    assert planner._defer_calls == [
        {'job': 'DailyJob', 'payload': {'task': 'data'}}
    ]
