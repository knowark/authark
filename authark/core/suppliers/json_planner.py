import schedulark
from typing import Callable, Dict
from ...application.general.suppliers import Planner


class JsonPlanner(Planner):
    def __init__(self, path: str) -> None:
        self.planner = schedulark.Planner(
            schedulark.JsonQueue(path))

    async def setup(self) -> None:
        await self.planner.setup()

    async def defer(self, job: str, payload: Dict = None) -> None:
        await self.planner.defer(job, payload)
