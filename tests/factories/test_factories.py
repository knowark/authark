import inspect
from injectark import Injectark
from authark.core.common import DEVELOPMENT_CONFIG
from authark.factories import factory_builder, strategy_builder


config = DEVELOPMENT_CONFIG

test_tuples = [
    ('BaseFactory', ['base']),
    ('CheckFactory', ['base', 'check']),
    ('CryptoFactory', ['base', 'crypto']),
    ('JsonFactory', ['base', 'crypto', 'json']),
]


def test_factories():

    for factory_name, strategy_names in test_tuples:
        factory = factory_builder.build(config, name=factory_name)
        strategy = strategy_builder.build(strategy_names)

        injector = Injectark(strategy=strategy, factory=factory)

        for resource in strategy.keys():
            result = injector.resolve(resource)
            classes = inspect.getmro(type(result))
            assert resource in [item.__name__ for item in classes]
