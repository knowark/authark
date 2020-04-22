# import inspect
# from pytest import fixture
# from injectark import Injectark
# from authark.infrastructure.config import build_config
# from authark.infrastructure.factories import build_strategy, build_factory
# from authark.infrastructure.factories import json_factory


# @fixture
# def mock_config():
#     config = build_config('DEV')
#     config['factory'] = 'JsonFactory'
#     return config


# @fixture
# def mock_strategy(mock_config):
#     strategy = build_strategy(['base', 'json'])
#     return strategy


# def test_json_factory(mock_config, mock_strategy):
#     factory = build_factory(mock_config)
#     resolver = Injectark(strategy=mock_strategy, factory=factory)

#     for resource in mock_strategy.keys():
#         result = resolver.resolve(resource)
#         classes = inspect.getmro(type(result))
#         assert resource in [item.__name__ for item in classes]
