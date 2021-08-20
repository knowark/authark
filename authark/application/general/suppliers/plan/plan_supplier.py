from typing import Dict, Callable
from abc import ABC, abstractmethod
from .jobs import Job
from .events import Event


class PlanSupplier(ABC):
    @abstractmethod
    async def setup(self) -> None:
        """Setup method to be implemented."""

    @abstractmethod
    async def defer(self, job: str, payload: Dict = None) -> None:
        """Defer method to be implemented."""

    @abstractmethod
    async def perform(self, job: Job) -> None:
        """Defer method to be implemented."""

    @abstractmethod
    async def notify(self, event: Event) -> None:
        """Defer method to be implemented."""


class MemoryPlanSupplier(PlanSupplier):
    def __init__(self) -> None:
        self._setup_calls: list = []
        self._defer_calls: list = []
        self._perform_calls: list = []
        self._notify_calls: list = []

    async def setup(self) -> None:
        self._setup_calls.append(True)

    async def defer(self, job: str, payload: Dict = None) -> None:
        self._defer_calls.append({'job': job, 'payload': payload})

    async def perform(self, job: Job) -> None:
        self._perform_calls.append(job)

    async def notify(self, event: Event) -> None:
        self._notify_calls.append(event)
