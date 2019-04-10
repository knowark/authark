from pytest import fixture, raises
from authark.application.services import (
    CatalogService, MemoryCatalogService, Tenant)


def test_catalog_service_methods():
    abstract_methods = CatalogService.__abstractmethods__

    assert 'setup' in abstract_methods


def test_memory_catalog_service_setup_catalog(catalog_service):
    catalog_service.setup()
    assert catalog_service.catalog == {}
