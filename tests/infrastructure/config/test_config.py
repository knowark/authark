import os
from json import JSONDecodeError
from pytest import raises
from authark.infrastructure.config import (
    TrialConfig, DevelopmentConfig, ProductionConfig)


def test_trial_config():
    config = TrialConfig()
    assert config['mode'] == 'TEST'


def test_development_config():
    config = DevelopmentConfig()
    assert config['mode'] == 'DEV'


# def test_production_config(tmpdir):
#     os.chdir(str(tmpdir))
#     with open('config.json', 'w') as f:
#         f.write('{"database": {"type": "postgresql"}}')
#     config = ProductionConfig()
#     assert config['mode'] == 'PROD'
#     assert config['database'] == {'type': 'postgresql'}


# def test_production_config_wrong_format(tmpdir):
#     os.chdir(str(tmpdir))
#     with open('config.json', 'w') as f:
#         f.write('<Bad></Bad>')
#     config = ProductionConfig()
#     assert config['mode'] == 'PROD'
#     assert config['database']['type'] == 'json'
