import json
from datetime import datetime
from pathlib import Path
from typing import List, Any
from ...application.services import TokenService, ExportService, Tenant


class JsonExportService(ExportService):

    def __init__(self, path: str, token_service: TokenService) -> None:
        self.path = path
        self.token_service = token_service

    def export_tenants(self, tenants: List[Tenant]) -> None:
        export_dict = {}
        for tenant in tenants:
            export_dict[tenant.slug] = (
                self.token_service.generate_token(vars(tenant)).value)

        path = Path(self.path)
        path.mkdir(parents=True, exist_ok=True)

        now = datetime.now().replace(microsecond=0).isoformat()
        now = now.replace('-', '').replace('T', '').replace(':', '')
        filepath = path / f"tenant_tokens_{now}.json"
        with filepath.open('w') as f:
            json.dump(export_dict, f, indent=2)
