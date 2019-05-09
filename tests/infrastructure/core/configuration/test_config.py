import os
from json import JSONDecodeError
from pytest import raises
from authark.infrastructure.core import (
    TrialConfig, DevelopmentConfig, ProductionConfig)


def test_trial_config():
    config = TrialConfig()
    assert config['mode'] == 'TEST'


def test_development_config():
    config = DevelopmentConfig()
    assert config['mode'] == 'DEV'
