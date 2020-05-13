from functools import partial
from injectark import Injectark
from ..schemas import PolicySchema
from .resource import Resource


class PolicyResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['AutharkInformer']
        manager = injector['SecurityManager']

        super().__init__(
            PolicySchema,
            partial(informer.count, 'policy'),
            partial(informer.search, 'policy'),
            manager.create_policy,
            manager.remove_policy)
