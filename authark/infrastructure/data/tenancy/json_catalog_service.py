import json
from pathlib import Path
from typing import Dict
from ....application.services import CatalogService, Tenant


class JsonCatalogService(CatalogService):

    def __init__(self, path: str) -> None:
        self.path = path
        self.catalog_schema: Dict = {
            'tenants': {}
        }

    def setup(self) -> bool:
        print('|||||| INSIDE JSON CATALOG SERVICE ||||||||||')
        catalog_file = Path(self.path)
        if catalog_file.exists():
            return False

        print('TO be created.....')
        with catalog_file.open('w') as f:
            json.dump(self.catalog_schema, f, indent=2)

        return True
