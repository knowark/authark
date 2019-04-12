from pytest import fixture, raises

from authark.application.utilities import ExpressionParser
from authark.application.reporters import TenancyReporter


def test_tenancy_reporter_methods():
    methods = TenancyReporter.__abstractmethods__
    assert 'search_tenants' in methods


def test_tenancy_reporter_search_tenants(tenancy_reporter):
    result = tenancy_reporter.search_tenants([])
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert len(result) == 1
