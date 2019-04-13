from pytest import fixture, raises
from authark.application.services import (
    TenantService, StandardTenantService, Tenant)


def test_tenant_service_methods():
    abstract_methods = TenantService.__abstractmethods__

    assert 'setup' in abstract_methods


def test_standard_tenant_service_instantiation(tenant_service):
    assert isinstance(tenant_service, TenantService)


def test_standard_tenant_service_setup(tenant_service):
    tenant = Tenant(name='Alpina')
    assert tenant_service.state.tenant is None
    tenant_service.setup(tenant)
    assert tenant_service.state.tenant == tenant


def test_standard_tenant_service_get_tenant(tenant_service):
    tenant = Tenant(name='Alpina')
    assert tenant_service.state.tenant is None
    tenant_service.setup(tenant)
    assert tenant_service.get_tenant() == tenant
