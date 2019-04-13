from typing import Dict
from pytest import fixture, raises
from authark.application.models import Permission, Grant
from authark.application.services import Tenant
from authark.application.utilities import ExpressionParser
from authark.application.coordinators import AffiliationCoordinator


def test_affiliation_coordinator_instantiation(affiliation_coordinator):
    assert affiliation_coordinator is not None


def test_affiliation_coordinator_establish_tenant(affiliation_coordinator):
    tenant_dict = {'slug': 'amazon'}
    affiliation_coordinator.catalog_service.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft')
    }
    affiliation_coordinator.establish_tenant(tenant_dict)
    tenant = affiliation_coordinator.tenant_service.get_tenant()
    assert tenant.slug == 'amazon'


def test_affiliation_coordinator_establish_tenant_not_found(
        affiliation_coordinator):
    tenant_dict = {'slug': 'Apple'}
    affiliation_coordinator.catalog_service.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft')
    }
    with raises(ValueError):
        affiliation_coordinator.establish_tenant(tenant_dict)
