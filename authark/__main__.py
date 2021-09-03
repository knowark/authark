"""
Authark entrypoint
"""
import sys
import asyncio
import uvloop
from injectark import Injectark
from .presentation.system.shell import Shell
from .integration.factories import factory_builder
from .integration.core import config, sanitize


config = sanitize(config)


async def main(args=None):
    factory = factory_builder.build(config)
    injector = Injectark(factory)
    await injector['SetupManager'].setup({})

    await Shell(config, injector).run(args or [])

    del injector
    await asyncio.gather(*asyncio.all_tasks())


if __name__ == '__main__':
    uvloop.install()
    asyncio.run(main(sys.argv[1:]))
