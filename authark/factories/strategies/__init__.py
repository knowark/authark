from injectark import StrategyBuilder
from .base import base
from .check import check
from .crypto import crypto
from .json import json


strategy_builder = StrategyBuilder({
    'base':  base,
    'check':  check,
    'crypto': crypto,
    'json': json
})
