import multiprocessing
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path


TEST = 'TEST'
DEV = 'DEV'
PROD = 'PROD'


class Config(dict, ABC):
    @abstractmethod
    def __init__(self):
        self['mode'] = 'BASE'
        self['environment'] = {
            'home': '/opt/authark'
        }
        self['gunicorn'] = {
            'bind': '%s:%s' % ('0.0.0.0', '8080'),
            'workers': 1,
            'worker_class': 'gevent',
            'debug': False
        }
        self['flask'] = {}
        self['database'] = {}
        self['tokens'] = {
            'access_lifetime': 86400,
            'refresh_lifetime': 604800,
            'refresh_threshold': 86400
        }


class TrialConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = TEST
        self['gunicorn'].update({
            'debug': True
        })


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = DEV
        self['gunicorn'].update({
            'debug': True,
            'accesslog': '-',
            'loglevel': 'debug'
        })


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = PROD
        self['gunicorn'].update({
            'debug': True,
            'accesslog': '-',
            'loglevel': 'debug'
        })
        self['database'] = {
            'type': 'json',
            'url': './authark_data.json'
        }
        self.read_configuration_files()

    def read_configuration_files(self):
        config_filename = '/config.json'
        paths = [
            '/etc/opt/authark' + config_filename,
            '/etc/authark' + config_filename,
            self['environment']['home'] + config_filename,
            '.' + config_filename
        ]
        for path in paths:
            config_dict = {}
            config_file = Path(path)
            if config_file.is_file():
                with config_file.open() as f:
                    try:
                        data = f.read()
                        config_dict = loads(data)
                    except JSONDecodeError:
                        pass
            self.update(config_dict)
