from pytest import fixture, raises
from authark.application.domain.common import QueryDomain
from authark.application.operation.informers import TenantInformer


async def test_tenant_informer_search_tenants(
        tenant_informer: TenantInformer, tenant_supplier) -> None:

    tenant_supplier.create_tenant({
        'id': '001',
        'name': 'Knowark'
    })
    domain: QueryDomain = []
    tenants = await tenant_informer.search_tenants({
        "meta":{
            "domain": domain
        }
    })
    assert len(tenants['data']) == 1
