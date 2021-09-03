
def test_tenant_manager(tenant_manager):
    assert hasattr(tenant_manager, 'create_tenant')


async def test_tenant_manager_create_tenant(
    tenant_manager, tenant_supplier):

    tenant_dict = {
        'id': '001',
        'name': 'Knowark'
    }

    await tenant_manager.create_tenant({
        "meta": {},
        "data": tenant_dict
    })

    assert tenant_supplier.get_tenant('001')['name'] == 'Knowark'
