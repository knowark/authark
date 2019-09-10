# from authark.application.services import Tenant
# from authark.application.coordinators import ExportCoordinator


# def test_export_coordinator_export_tenants(
#         export_coordinator: ExportCoordinator) -> None:
#     tenant_ids = ['001', '003']
#     export_coordinator.catalog_service.catalog = {  # type: ignore
#         '001': Tenant(id='001', name='Amazon'),
#         '002': Tenant(id='002', name='Google'),
#         '003': Tenant(id='003', name='Microsoft'),
#     }
#     export_coordinator.export_tenants(tenant_ids)
#     tenants = export_coordinator.export_service.tenants  # type:ignore
#     for tenant in tenants:
#         assert tenant.id in tenant_ids
