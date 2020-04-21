from typing import Dict, Any
from ..config import Config
from .factory import Factory
from .memory_factory import MemoryFactory
from .crypto_factory import CryptoFactory
from .json_factory import JsonFactory
from .check_factory import CheckFactory
from .strategies import build_strategy


def build_factory(config: Config) -> Factory:
    factory = config['factory']
    return {
        'MemoryFactory': lambda config: MemoryFactory(config),
        'CryptoFactory': lambda config: CryptoFactory(config),
        'JsonFactory': lambda config: JsonFactory(config),
        'CheckFactory': lambda config: CheckFactory(config)
    }[factory](config)
