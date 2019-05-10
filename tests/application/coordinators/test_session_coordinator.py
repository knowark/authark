import jwt
from typing import Dict, cast
from pytest import fixture
from authark.application.services import (
    TenantService, StandardTenantService, Tenant)
from authark.application.coordinators import SessionCoordinator


def test_session_coordinator_creation(
        session_coordinator: SessionCoordinator) -> None:
    assert hasattr(session_coordinator, 'set_tenant')


def test_session_coordinator_set_tenant(session_coordinator):
    tenant = {'name': 'Amazon'}
    session_coordinator.set_tenant(tenant)
    tenant = session_coordinator.tenant_service.tenant
    assert tenant.slug == 'amazon'


def test_session_coordinator_get_tenant(session_coordinator):
    tenant = {'name': 'Amazon'}
    session_coordinator.set_tenant(tenant)
    tenant = session_coordinator.get_tenant()
    assert tenant['slug'] == 'amazon'
