from typing import List, Callable
from injectark import Injectark
from ....integration.core import Config
from .authenticate import authenticate_middleware_factory
from .errors import errors_middleware_factory


def middlewares(config: Config, injector: Injectark) -> List[Callable]:
    return [
        errors_middleware_factory(config, injector),
        authenticate_middleware_factory(config, injector)
    ]
