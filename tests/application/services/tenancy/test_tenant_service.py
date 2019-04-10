from pytest import fixture, raises
from authark.application.services import (
    TenantService, StandardTenantService, Tenant, CatalogService)


def test_tenant_service_methods():
    abstract_methods = TenantService.__abstractmethods__


def test_standard_tenant_service_instantiation(tenant_service):
    assert isinstance(tenant_service, TenantService)
    assert isinstance(tenant_service.catalog_service, CatalogService)
