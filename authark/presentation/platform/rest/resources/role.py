from functools import partial
from injectark import Injectark
from ..schemas import RoleSchema
from .resource import Resource


class RoleResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['AutharkInformer']
        manager = injector['ManagementManager']

        super().__init__(
            RoleSchema,
            partial(informer.count, 'role'),
            partial(informer.search, 'role'),
            manager.create_role,
            manager.remove_role)
