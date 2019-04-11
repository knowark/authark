from pytest import fixture, raises
from authark.application.services import (
    ProvisionService, MemoryProvisionService, Tenant)


# def test_provision_service_methods():
#     abstract_methods = ProvisionService.__abstractmethods__

#     assert 'setup' in abstract_methods


# def test_memory_provision_service_setup_provision(provision_service):
#     provision_service.setup()
#     assert provision_service.pool == {}
