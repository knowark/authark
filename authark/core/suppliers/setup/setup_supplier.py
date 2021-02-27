from abc import ABC, abstractmethod


class SetupSupplier(ABC):
    @abstractmethod
    def setup(self) -> None:
        """Setup on start method to be implemented."""


class MemorySetupSupplier(SetupSupplier):
    def setup(self):
        pass
