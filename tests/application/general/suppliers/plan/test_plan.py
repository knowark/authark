from pytest import raises
from authark.application.general import PlanSupplier, MemoryPlanSupplier


def test_plan_supplier_methods() -> None:
    methods = PlanSupplier.__abstractmethods__  # type: ignore
    assert 'setup' in methods
    assert 'defer' in methods


async def test_memory_plan_supplier_setup() -> None:
    planner = MemoryPlanSupplier()

    await planner.setup()

    assert planner._setup_calls == [True]


async def test_memory_plan_supplier_defer() -> None:
    planner = MemoryPlanSupplier()

    await planner.defer('DailyJob', {'task': 'data'})

    assert planner._defer_calls == [
        {'job': 'DailyJob', 'payload': {'task': 'data'}}
    ]
