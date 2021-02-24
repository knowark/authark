"""
Authark entrypoint
"""
import sys
import asyncio
import uvloop
from injectark import Injectark
from .presenters.shell import Shell
from .factories import factory_builder, strategy_builder
from .core import config


async def main(args=None):
    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(factory, strategy)
    injector['SetupSupplier'].setup()

    await Shell(config, injector).run(args or [])


if __name__ == '__main__':
    uvloop.install()
    asyncio.run(main(sys.argv[1:]))
