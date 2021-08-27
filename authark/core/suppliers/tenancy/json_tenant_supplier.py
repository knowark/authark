from pathlib import Path
from typing import Dict
from tenark.resolver import resolve_managers
from ....application.general.suppliers import MemoryTenantSupplier


class JsonTenantSupplier(MemoryTenantSupplier):

    def __init__(self, catalog_path: str, zones: Dict[str, str],
                 directory_template='__template__') -> None:
        directory_template = str(Path(zones['default']) / '__template__')
        self.arranger, self.provider = resolve_managers({
            'cataloguer_kind': 'json',
            'catalog_path': catalog_path,
            'provisioner_kind': 'directory',
            'provision_template': directory_template,
            'provision_directory_zones': zones
        })
