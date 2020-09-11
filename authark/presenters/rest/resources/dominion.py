from functools import partial
from injectark import Injectark
from ..schemas import DominionSchema
from ..helpers import missing
from .resource import Resource


class DominionResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['AutharkInformer']

        super().__init__(
            DominionSchema,
            partial(informer.count, 'dominion'),
            partial(informer.search, 'dominion'),
            missing,
            missing)
