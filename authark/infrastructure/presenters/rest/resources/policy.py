from functools import partial
from injectark import Injectark
from ..schemas import PolicySchema
from .resource import Resource


class PolicyResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['AutharkInformer']
        manager = injector['AuthManager']

        super().__init__(
            PolicySchema,
            partial(informer.count, 'policy'),
            partial(informer.search, 'policy'),
            manager.register,
            manager.deregister)
