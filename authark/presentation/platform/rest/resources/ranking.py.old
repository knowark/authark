from functools import partial
from injectark import Injectark
from ..schemas import RankingSchema
from .resource import Resource


class RankingResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['AutharkInformer']
        manager = injector['ManagementManager']
        super().__init__(
            RankingSchema,
            partial(informer.count, 'ranking'),
            partial(informer.search, 'ranking'),
            manager.assign_role,
            manager.deassign_role)
