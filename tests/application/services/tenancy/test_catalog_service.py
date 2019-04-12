from pytest import fixture, raises
from authark.application.services import (
    CatalogService, MemoryCatalogService, Tenant)


def test_catalog_service_methods():
    abstract_methods = CatalogService.__abstractmethods__

    assert 'setup' in abstract_methods


def test_memory_catalog_service_setup_catalog(catalog_service):
    catalog_service.setup()
    assert catalog_service.catalog == {}


def test_memory_catalog_service_add_tenant(catalog_service):
    tenant = Tenant(name='Microsoft')
    catalog_service.setup()
    tenant = catalog_service.add_tenant(tenant)
    assert len(catalog_service.catalog) == 1


def test_memory_catalog_service_add_tenant_no_setup(catalog_service):
    tenant = Tenant(name='Microsoft')
    with raises(ValueError):
        catalog_service.add_tenant(tenant)


def test_memory_catalog_service_search_tenants_empty(catalog_service):
    tenant = Tenant(name='Microsoft')
    catalog_service.setup()
    tenants = catalog_service.search_tenants([])
    assert len(tenants) == 0


def test_memory_catalog_service_search_tenants(
        catalog_service: MemoryCatalogService):
    tenant = Tenant(name='Microsoft')
    catalog_service.setup()
    catalog_service.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft'),
    }
    tenants = catalog_service.search_tenants(
        [('slug', '=', 'amazon')])
    assert len(tenants) == 1
