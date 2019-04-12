from pytest import raises
from typing import cast
from authark.application.services import (
    Tenant, MemoryCatalogService, MemoryProvisionService)
from authark.application.coordinators import (
    SetupCoordinator, TenantAlreadyExistsError)


def test_setup_coordinator_creation(
        setup_coordinator: SetupCoordinator) -> None:
    assert hasattr(SetupCoordinator, 'setup_server')
    assert hasattr(SetupCoordinator, 'create_tenant')


def test_setup_coordinator_setup_server(
        setup_coordinator: SetupCoordinator) -> None:
    catalog_service = cast(MemoryCatalogService,
                           setup_coordinator.catalog_service)
    provision_service = cast(MemoryProvisionService,
                             setup_coordinator.provision_service)
    assert catalog_service.catalog is None
    assert provision_service.pool is None
    setup_coordinator.setup_server()
    assert catalog_service.catalog == {}
    assert provision_service.pool == {}


def test_setup_coordinator_create_tenant(
        setup_coordinator: SetupCoordinator) -> None:
    provision_service = cast(MemoryProvisionService,
                             setup_coordinator.provision_service)
    tenant_dict = {"name": "Google"}
    setup_coordinator.setup_server()
    setup_coordinator.create_tenant(tenant_dict)
    assert len(provision_service.pool) == 1


def test_setup_coordinator_create_tenant_duplicate(
        setup_coordinator: SetupCoordinator) -> None:
    provision_service = cast(MemoryProvisionService,
                             setup_coordinator.provision_service)
    catalog_service = cast(MemoryCatalogService,
                           setup_coordinator.catalog_service)
    setup_coordinator.setup_server()
    catalog_service.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft'),
    }

    tenant_dict = {"name": "Google"}
    with raises(TenantAlreadyExistsError):
        setup_coordinator.create_tenant(tenant_dict)
