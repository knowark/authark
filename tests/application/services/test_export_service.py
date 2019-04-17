from inspect import signature
from authark.application.services import (
    ExportService, MemoryExportService, Tenant)


def test_export_service() -> None:
    methods = ExportService.__abstractmethods__  # type: ignore
    assert 'export_tenants' in methods


def test_memory_export_service_implementation() -> None:
    assert issubclass(MemoryExportService, ExportService)


def test_memory_export_service_export_tenants() -> None:
    export_service = MemoryExportService()
    tenants = [Tenant(name='Éxito'), Tenant(name='Olímpica')]
    export_service.export_tenants(tenants)

    assert export_service.tenants == tenants
