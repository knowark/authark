"""
Authark entrypoint
"""
import sys
import os
from injectark import Injectark
from .infrastructure.core import build_config, build_factory
from .infrastructure.cli import Cli


def main():  # pragma: no cover
    mode = os.environ.get('AUTHARK_MODE', 'PROD')
    config_path = os.environ.get('AUTHARK_CONFIG', 'config.json')
    config = build_config(config_path, mode)

    factory = build_factory(config)
    strategy = config['strategy']
    resolver = Injectark(strategy=strategy, factory=factory)

    Cli(config, resolver).run(sys.argv[1:])


if __name__ == '__main__':  # pragma: no cover
    main()
