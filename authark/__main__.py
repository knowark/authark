"""
Authark entrypoint
"""
import os
import sys
import asyncio
import logging
import uvloop
from json import loads
from pathlib import Path
from injectark import Injectark
from .factories import factory_builder, strategy_builder
from .presenters.shell import Shell
from .core import config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main(args=None):
    # config_path = Path(os.environ.get('AUTHARK_CONFIG', 'config.json'))
    # logger.info(f'Configuration: {config_path}')
    # config = loads(config_path.read_text()) if config_path.is_file() else {}
    # config: Config = {**PRODUCTION_CONFIG, **config}

    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)
    injector['SetupSupplier'].setup()

    await Shell(config, injector).run(args or [])


if __name__ == '__main__':
    uvloop.install()
    asyncio.run(main(sys.argv[1:]))
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(sys.argv[1:]))
    # loop.close()
