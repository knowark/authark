from typing import Dict, Any
from .memory_factory import MemoryFactory
from .crypto_factory import CryptoFactory
from .json_factory import JsonFactory
from ..config import Config


def build_factories(config: Config) -> Dict[str, Any]:
    return {
        'MemoryFactory': MemoryFactory(config),
        'CryptoFactory': CryptoFactory(config),
        'JsonFactory': JsonFactory(config)
    }
