"""
Authark entrypoint
"""

import os
from injectark import Injectark
from .infrastructure.config import build_config
from .infrastructure.factories import build_factory
from .infrastructure.cli import Cli


def main():  # pragma: no cover
    mode = os.environ.get('AUTHARK_MODE', 'PROD')
    config_path = os.environ.get('AUTHARK_CONFIG', 'authark_config.json')
    config = build_config(config_path, mode)
    print('ccc', config_path)

    factory = build_factory(config)
    strategy = config['strategy']
    resolver = Injectark(strategy=strategy, factory=factory)

    Cli(config, resolver)


if __name__ == '__main__':  # pragma: no cover
    main()
