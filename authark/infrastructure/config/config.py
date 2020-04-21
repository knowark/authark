import multiprocessing
from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path


class Config(defaultdict, ABC):
    @abstractmethod
    def __init__(self):
        self["mode"] = "BASE"
        self['environment'] = {
            'home': '/opt/authark'
        }
        self["port"] = 6291
        self['tokens'] = {
            'tenant': {
                'algorithm': 'HS256',
                'secret': 'DEVSECRET123',
                'lifetime': 86400
            },
            'access': {
                'algorithm': 'HS256',
                'secret': 'DEVSECRET123',
                'lifetime': 86400
            },
            'refresh': {
                'algorithm': 'HS256',
                'secret': 'DEVSECRET123',
                'lifetime': 604800,
                'threshold': 86400
            }
        }
        self['strategies'] = ['base']
        self['strategy'] = {}
        self["tenancy"] = {
            "dsn": "",
            "directory": ""
        }

        self["zones"] = {
            "default": {
                "dsn": "",
                "directory": ""
            }
        }


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self["mode"] = "DEV"
        self['factory'] = 'CheckFactory'
        self['strategies'].extend(['check'])


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = "PROD"
        self["factory"] = "JsonFactory"
        self['strategies'].extend(['json'])
        self['tenancy'] = {
            "json": Path.home() / 'tenants.json',
            "directory" : ""
        }
        self['data'] = {
            "json": {
                "default": str(Path.home() / 'data')
            }
        }
        self['export'] = {
            'type': 'json',
            'dir': Path.home() / 'export'
        }
        # self["tenancy"] = {
        #     "dsn": (
        #         "postgresql://authark:authark"
        #         "@localhost/authark"),
        #     "directory": ""
        # }
        self["zones"] = {
            "default": {
                "dsn": ("postgresql://authark:authark"
                        "@localhost/authark"),
                "directory": ""
            }
        }
