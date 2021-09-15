import schedulark
from typing import Callable, Dict
from .....application.general.suppliers import (
    PlanSupplier, Job, Event)


class JsonPlanSupplier(PlanSupplier):
    def __init__(self, path: str) -> None:
        self.planner = schedulark.Planner(
            schedulark.JsonQueue(path))

    async def setup(self) -> None:
        await self.planner.setup()

    async def defer(self, job: str, payload: Dict = None) -> None:
        await self.planner.defer(job, payload)

    async def perform(self, job: Job) -> None:
        job_name = job.__class__.__name__
        payload = {'meta': {}, 'data': vars(job)}
        await self.planner.defer(job_name, payload)

    async def notify(self, event: Event) -> None:
        event_meta = {
            'name': event.__class__.__name__
        }
        event_data = vars(event)
        payload = {
            'meta': {
                'event': event_meta,
                'authorization': str(event_data.pop('authorization'))
            }, 'data': event_data
        }
        await self.planner.defer('NotifyJob', payload)
