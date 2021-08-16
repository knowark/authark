from typing import Dict, Callable
from abc import ABC, abstractmethod


class Planner(ABC):
    @abstractmethod
    async def setup(self) -> None:
        """Setup method to be implemented."""

    @abstractmethod
    async def defer(self, job: str, payload: Dict = None) -> None:
        """Defer method to be implemented."""


class MemoryPlanner(Planner):
    def __init__(self) -> None:
        self._setup_calls: list = []
        self._defer_calls: list = []

    async def setup(self) -> None:
        self._setup_calls.append(True)

    async def defer(self, job: str, payload: Dict = None) -> None:
        self._defer_calls.append({'job': job, 'payload': payload})
