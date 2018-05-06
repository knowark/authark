import multiprocessing
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path
from authark.infrastructure.config.registry import (
    Registry
)

TEST = 'TEST'
DEV = 'DEV'
PROD = 'PROD'

REGISTRY_DICT = {
    DEV: Registry,
}


class Config(dict, ABC):
    @abstractmethod
    def __init__(self):
        self['mode'] = 'BASE'
        self['environment'] = {
            'home': '/opt/serproser'
        }
        self['gunicorn'] = {
            'bind': '%s:%s' % ('0.0.0.0', '8080'),
            'workers': 1,
            'worker_class': 'gevent',
            'debug': False
        }
        self['flask'] = {}
        self['database'] = {}
        self['registry'] = {}

    def resolve_registry(self) -> None:
        registry = REGISTRY_DICT[self['mode']]
        self['registry'] = registry(self)


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = DEV
        self['gunicorn'].update({
            'debug': True
        })
