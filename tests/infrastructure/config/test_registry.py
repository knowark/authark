import os
from json import JSONDecodeError
from pytest import raises
from authark.infrastructure.config.config import (
    TrialConfig, DevelopmentConfig, ProductionConfig)
from authark.infrastructure.config.registry import (
    MemoryRegistry, JsonJwtRegistry)
from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.application.reporters.authark_reporter import AutharkReporter


def test_memory_registry():
    config = TrialConfig()
    registry = MemoryRegistry(config)
    assert isinstance(registry['auth_coordinator'], AuthCoordinator)
    assert isinstance(registry['auth_reporter'], AutharkReporter)


def test_json_jwt_registry():
    config = ProductionConfig()
    registry = JsonJwtRegistry(config)
    assert isinstance(registry['auth_coordinator'], AuthCoordinator)
    assert isinstance(registry['auth_reporter'], AutharkReporter)
