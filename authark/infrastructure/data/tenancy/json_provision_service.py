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

    def setup(self) -> bool:

        directory = Path(self.directory)
        if directory.exists():
            return False

        print('Provisioning data setup...', str(directory))
        directory.mkdir(parents=True)

        return True

    def provision_tenant(self, tenant: Tenant) -> None:
        filepath = Path(self.directory) / tenant.slug / f"{tenant.slug}.json"
        self._deploy_schema(filepath, self.collections)

    def _deploy_schema(self, filepath: Path, collections: List[str]) -> None:
        parent_path = Path(filepath).parent
        parent_path.mkdir(parents=True, exist_ok=True)
        filepath.touch()

        with filepath.open('r') as f:
            content = f.read() or "{}"
            data = json.loads(content)

            for collection in collections:
                if collection not in data:
                    data[collection] = {}

            with filepath.open('w') as f:
                json.dump(data, f, indent=2)
