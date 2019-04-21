from typing import Dict
from pytest import fixture, raises
from authark.application.models import Permission, Grant
from authark.application.services import Tenant
from authark.application.utilities import ExpressionParser
from authark.application.coordinators import AffiliationCoordinator


def test_affiliation_coordinator_instantiation(affiliation_coordinator):
    assert affiliation_coordinator is not None


def test_affiliation_coordinator_establish_tenant(affiliation_coordinator):
    tenant_id = '001'
    affiliation_coordinator.catalog_service.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft')
    }
    affiliation_coordinator.establish_tenant(tenant_id)
    tenant = affiliation_coordinator.tenant_service.get_tenant()
    assert tenant.slug == 'amazon'


def test_affiliation_coordinator_get_current_tenant(affiliation_coordinator):
    affiliation_coordinator.tenant_service.state.tenant = (
        Tenant(id='001', name='Amazon'))

    current_tenant = affiliation_coordinator.get_current_tenant()
    assert isinstance(current_tenant, dict)
    assert current_tenant.get('id') == '001'
    assert current_tenant.get('name') == 'Amazon'


def test_affiliation_coordinator_resolve_tenant(affiliation_coordinator):
    affiliation_coordinator.catalog_service.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft')
    }
    affiliation_coordinator.resolve_tenant('microsoft')
    tenant = affiliation_coordinator.tenant_service.get_tenant()
    assert tenant.slug == 'microsoft'

    affiliation_coordinator.resolve_tenant('Google')
    tenant = affiliation_coordinator.tenant_service.get_tenant()
    assert tenant.slug == 'google'
