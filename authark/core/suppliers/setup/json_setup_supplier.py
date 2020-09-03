from typing import Dict, Any
from pathlib import Path
from .memory_setup_supplier import MemorySetupSupplier


class JsonSetupSupplier(MemorySetupSupplier):
    def __init__(self, zones: Dict[str, Any]) -> None:
        self.zones = zones

    def setup(self):
        base_path = Path(self.zones['default'])
        provision_directory = base_path / '__template__'
        provision_directory.mkdir(exist_ok=True, parents=True)
