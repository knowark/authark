from typing import cast
from authark.application.models import User
from authark.application.services import MemoryCatalogService
from authark.application.coordinators import SetupCoordinator


def test_setup_coordinator_creation(
        setup_coordinator: SetupCoordinator) -> None:
    assert hasattr(SetupCoordinator, 'setup_catalog')
    assert hasattr(SetupCoordinator, 'create_tenant')


def test_setup_coordinator_setup_catalog(
        setup_coordinator: SetupCoordinator) -> None:
    catalog_service = cast(MemoryCatalogService,
                           setup_coordinator.catalog_service)
    assert catalog_service.catalog is None
    setup_coordinator.setup_catalog()
    assert catalog_service.catalog == {}


def test_setup_coordinator_create_tenant(
        setup_coordinator: SetupCoordinator) -> None:
    catalog_service = cast(MemoryCatalogService,
                           setup_coordinator.catalog_service)
    assert catalog_service.catalog is None
    setup_coordinator.setup_catalog()
    assert catalog_service.catalog == {}
