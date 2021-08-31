from functools import partial
from injectark import Injectark
from ..schemas import RestrictionSchema
from .resource import Resource


class RestrictionResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['AutharkInformer']
        manager = injector['SecurityManager']

        super().__init__(
            RestrictionSchema,
            partial(informer.count, 'restriction'),
            partial(informer.search, 'restriction'),
            manager.create_restriction,
            manager.remove_restriction)
