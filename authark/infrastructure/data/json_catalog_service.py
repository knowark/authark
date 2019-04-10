from ...application.services import CatalogService, Tenant


class JsonCatalogService(CatalogService):

    def __init__(self) -> None:
        pass

    def setup(self) -> bool:
        print('|||||| INSIDE JSON CATALOG SERVICE ||||||||||')
        return True
