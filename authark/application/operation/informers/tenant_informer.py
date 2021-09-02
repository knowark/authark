from abc import ABC, abstractmethod
from ...general.suppliers.tenancy import TenantSupplier


class TenantInformer(ABC):
    def __init__(self, tenant_supplier: TenantSupplier) -> None:
        self.tenant_supplier = tenant_supplier

    async def search_tenants(self, entry: dict) -> dict:
        meta = entry['meta']
        result = self.tenant_supplier.search_tenants(meta['domain'])
        return {'data': result}
