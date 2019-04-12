from pytest import fixture, raises
from authark.application.services import (
    ProvisionService, MemoryProvisionService, Tenant)


def test_provision_service_methods():
    abstract_methods = ProvisionService.__abstractmethods__

    assert 'setup' in abstract_methods
    assert 'provision_tenant' in abstract_methods


def test_memory_provision_service_setup(provision_service):
    provision_service.setup()
    assert provision_service.pool == {}


def test_memory_provision_service_provision_tenant(provision_service):
    tenant = Tenant(name="Servagro")
    provision_service.setup()
    provision_service.provision_tenant(tenant)
    assert len(provision_service.pool) == 1


def test_memory_provision_service_provision_tenant_no_setup(provision_service):
    tenant = Tenant(name="Servagro")
    with raises(ValueError):
        provision_service.provision_tenant(tenant)
