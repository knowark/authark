from typing import Dict, Any
from ..config import Config
from .factory import Factory
from .memory_factory import MemoryFactory
from .crypto_factory import CryptoFactory
from .json_factory import JsonFactory


def build_factory(config: Config) -> Factory:
    return {
        'MemoryFactory': MemoryFactory(config),
        'CryptoFactory': CryptoFactory(config),
        'JsonFactory': JsonFactory(config)
    }.get(config.get('factory', 'MemoryFactory'))
