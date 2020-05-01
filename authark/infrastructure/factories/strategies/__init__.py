from injectark import StrategyBuilder
from .base import base
from .check import check
from .json import json


strategy_builder = StrategyBuilder({
    'base':  base,
    'check':  check,
    'json': json
})
