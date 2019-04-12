from ....application.models import Policy
from ....application.utilities import ExpressionParser
from ....application.repositories import PolicyRepository
from .json_repository import JsonRepository


class JsonPolicyRepository(
        JsonRepository[Policy], PolicyRepository):
    """Json Policy Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 collection_name: str = 'policies') -> None:
        super().__init__(file_path, parser, collection_name, Policy)
