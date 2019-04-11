import json
from pathlib import Path
from typing import Dict, List, Any
from ....application.services import ProvisionService, Tenant


class JsonProvisionService(ProvisionService):

    def __init__(self, directory: str) -> None:
        self.directory = directory
        self.collections = [
            'users',
            'credentials',
            'dominions',
            'roles',
            'rankings',
            'policies',
            'permissions',
            'resources',
            'grants'
        ]

        print('||||| Provision directory>>>', self.directory)

    def setup(self) -> bool:

        directory = Path(self.directory)
        if directory.exists():
            return False

        print('Provisioning data setup...', str(directory))
        directory.mkdir(parents=True)

        return True

    def create_tenant(self, tenant: Tenant) -> Tenant:
        print('Calling provision json...')

    #     tenant = self._register_tenant(tenant)

    # def _deploy_schema(self, filename: str, collections: List[str]) -> None:
    #     parent_path = Path(filename).parent
    #     parent_path.mkdir(parents=True, exist_ok=True)
    #     filepath = Path(filename)
    #     filepath.touch()

    #     with filepath.open('r') as f:
    #         content = f.read() or "{}"
    #         data = json.loads(content)

    #         for collection in collections:
    #             if collection not in data:
    #                 data[collection] = {}

    #         with filepath.open('w') as f:
    #             json.dump(data, f)
