from pytest import raises
from authark.application.general import (
    PlanSupplier, MemoryPlanSupplier, Event, Job)


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


async def test_memory_plan_supplier_notify() -> None:
    planner = MemoryPlanSupplier()

    class CustomEvent(Event):
        """Custom Application Event"""

    event = CustomEvent(reference_id='R001', quantity=777)
    await planner.notify(event)

    assert planner._notify_calls == [event]


async def test_memory_plan_supplier_perform() -> None:
    planner = MemoryPlanSupplier()

    class CustomJob(Job):
        """Custom Application Job"""

    job = CustomJob(delay=3_600)
    await planner.perform(job)

    assert planner._perform_calls == [job]
