import json
from uuid import uuid4
from pathlib import Path
from typing import Dict, List, Any
from ....application.utilities import QueryDomain
from ....application.services import CatalogService, Tenant


class JsonCatalogService(CatalogService):

    def __init__(self, path: str) -> None:
        self.path = path
        self.collection_name = 'tenants'
        self.catalog_schema: Dict = {
            self.collection_name: {}
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

    def add_tenant(self, tenant: Tenant) -> Tenant:
        data: Dict[str, Any] = {}
        with open(self.path, 'r') as f:
            data = json.load(f)

        tenant.id = tenant.id or str(uuid4())
        data[self.collection_name].update({tenant.id: vars(tenant)})
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=2)

        return tenant

    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        return []
