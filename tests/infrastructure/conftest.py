# from pytest import fixture
# from injectark import Injectark
# from authark.infrastructure.core import TrialConfig, build_factory
# from authark.infrastructure.terminal.framework import Context


# @fixture
# def config():
#     return TrialConfig()


# @fixture
# def resolver(config):
#     factory = build_factory(config)
#     strategy = config['strategy']
#     resolver = Injectark(strategy=strategy, factory=factory)
#     return resolver


# @fixture
# def context(config, registry):
#     return Context(config, registry)
