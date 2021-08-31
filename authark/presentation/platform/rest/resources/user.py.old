from functools import partial
from injectark import Injectark
from ..schemas import UserSchema
from .resource import Resource


class UserResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['AutharkInformer']
        manager = injector['ProcedureManager']

        super().__init__(
            UserSchema,
            partial(informer.count, 'user'),
            partial(informer.search, 'user'),
            manager.update,
            manager.deregister)
