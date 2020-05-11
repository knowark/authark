from functools import partial
from injectark import Injectark
from ..schemas import RuleSchema
from .resource import Resource


class RuleResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['AutharkInformer']
        manager = injector['AuthManager']

        super().__init__(
            RuleSchema,
            partial(informer.count, 'rule'),
            partial(informer.search, 'rule'),
            manager.register,
            manager.deregister)
