"""
Authark entrypoint
"""

import os
import sys
import asyncio
import uvloop
from injectark import Injectark
# from authark.infrastructure.config import build_config
# from authark.infrastructure.factories import build_factory, build_strategy
from .infrastructure.presentation.cli import Cli


async def main(args=None):
    config_path = os.environ.get('AUTHARK_CONFIG', 'config.json')
    # config = build_config('PROD', config_path)

    # factory = build_factory(config)
    # strategy = build_strategy(config['strategies'], config['strategy'])
    # injector = Injectark(strategy=strategy, factory=factory)
    # injector['SetupSupplier'].setup()

    # await Cli(config, injector).run(args or [])


if __name__ == '__main__':
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv[1:]))
    loop.close()
