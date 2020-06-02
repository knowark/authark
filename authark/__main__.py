"""
Authark entrypoint
"""
import os
import sys
import asyncio
import uvloop
from json import loads
from pathlib import Path
from injectark import Injectark
from .core import Config, PRODUCTION_CONFIG
from .factories import factory_builder, strategy_builder
from .presenters.shell import Shell


async def main(args=None):
    config_path = Path(os.environ.get('AUTHARK_CONFIG', 'config.json'))
    config = loads(config_path.read_text()) if config_path.is_file() else {}
    config: Config = {**PRODUCTION_CONFIG, **config}

    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)

    await Shell(config, injector).run(args or [])


if __name__ == '__main__':
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv[1:]))
    loop.close()
