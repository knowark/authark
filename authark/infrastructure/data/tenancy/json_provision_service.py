import json
from pathlib import Path
from typing import Dict
from ....application.services import ProvisionService, Tenant


class JsonProvisionService(ProvisionService):

    def __init__(self, directory: str) -> None:
        self.directory = directory

        print('||||| Provision directory>>>', self.directory)

    def setup(self):

        directory = Path(self.directory)
        if directory.exists():
            return False

        print('Provisioning data setup...', str(directory))
        directory.mkdir(parents=True)

        return True

    def create_tenant(self, tenant):
        return super().create_tenant(tenant)
