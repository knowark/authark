from pytest import fixture
from authark.infrastructure.resolver import Resolver, Config


class FooRepository:
    pass


class MemoryFooRepository(FooRepository):
    pass


class BarRepository:
    pass


class MemoryBarRepository(BarRepository):
    pass


class StandardBazService:
    def __init__(self, foo_repository: FooRepository,
                 bar_repository: BarRepository):
        self.foo_repository = foo_repository
        self.bar_repository = bar_repository


@fixture
def config():
    config = {
        'factory': 'MockFactory'
    }
    return config


@fixture
def mock_factory():
    class MockFactory:

        def memory_foo_repository(self):
            return MemoryFooRepository()

        def memory_bar_repository(self):
            return MemoryBarRepository()

        def standard_baz_service(self, foo_repository: FooRepository,
                                 bar_repository: BarRepository):
            return StandardBazService(foo_repository, bar_repository)

        def dedicated_foo_repository(self):
            return MemoryFooRepository()

    return MockFactory()


@fixture
def providers_dict():
    return {
        "FooRepository": {
            "method": "memory_foo_repository"
        },
        "BarRepository": {
            "method": "memory_bar_repository"
        },
        "BazService": {
            "method": "standard_baz_service"
        }
    }


@fixture
def dedicated_providers_dict():
    return {
        "FooRepository": {
            "method": "memory_foo_repository"
        },
        "BarRepository": {
            "method": "memory_bar_repository"
        },
        "BazService": {
            "method": "standard_baz_service",
            "providers": {
                "FooRepository": "dedicated_foo_repository"
            }
        }
    }


@fixture
def factories(mock_factory):
    return {
        'MockFactory': mock_factory
    }


@fixture
def resolver(config, factories):
    resolver = Resolver(config, factories)
    return resolver
