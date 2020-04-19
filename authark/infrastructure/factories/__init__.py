from typing import Dict, Any
from ..config import Config
from .factory import Factory
from .memory_factory import MemoryFactory
from .crypto_factory import CryptoFactory
from .json_factory import JsonFactory
from .http_factory import HttpFactory
from .web_factory import WebFactory


def build_factory(config: Config) -> Factory:
    factory = config['factory']
    return {
        'MemoryFactory': lambda config: MemoryFactory(config),
        'CryptoFactory': lambda config: CryptoFactory(config),
        'JsonFactory': lambda config: JsonFactory(config),
        'HttpFactory': lambda config: HttpFactory(config),
        'WebFactory': lambda config: WebFactory(config)
    }[factory](config)
