
from ...general.suppliers import SetupSupplier


class SetupManager:
    def __init__(
        self, setup_supplier: SetupSupplier
    ) -> None:
        self.setup_supplier = setup_supplier

    async def setup(self, entry: dict) -> dict:

        self.setup_supplier.setup()

        return {}
