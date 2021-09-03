from ...general.suppliers import TenantSupplier


class TenantManager:
    def __init__(
        self, tenant_supplier: TenantSupplier
    ) -> None:
        self.tenant_supplier = tenant_supplier

    async def create_tenant(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        self.tenant_supplier.create_tenant(data)

        return {}

    async def resolve_tenant(self, entry: dict) -> dict:
        return {"data": self.tenant_supplier.resolve_tenant(entry['data'])}
