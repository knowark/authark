from functools import partial
from injectark import Injectark
from ..helpers import UserSchema
from .resource import Resource


class UserResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['AutharkInformer']
        manager = injector['AuthManager']

        super().__init__(
            UserSchema,
            partial(informer.count, 'user'),
            partial(informer.search, 'user'),
            manager.register,
            manager.deregister)
