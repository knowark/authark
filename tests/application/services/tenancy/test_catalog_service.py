from pytest import fixture, raises
from authark.application.services import (
    CatalogService, MemoryCatalogService, Tenant)


def test_catalog_service_methods():
    abstract_methods = CatalogService.__abstractmethods__

    # assert 'setup' in abstract_methods
    # assert 'is_authenticated' in abstract_methods
    # assert 'validate_roles' in abstract_methods
    # assert 'get_user' in abstract_methods
