from pytest import fixture
from authark.application.domain.common import (
    TenantProvider, StandardTenantProvider)


@fixture
def tenant_provider() -> TenantProvider:
    return StandardTenantProvider()
