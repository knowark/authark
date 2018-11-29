"""
Authark entrypoint
"""
import sys
import argparse
from typing import Type
from authark.infrastructure.web.base import create_app
from authark.infrastructure.terminal.main import Main


# def main() -> None:  # pragma: no cover
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "-dev", "--developement",
#         help="Development Mode.",
#         action="store_true")
#     parser.add_argument(
#         "-t", "--terminal",
#         help="Terminal User Interface.",
#         action="store_true")
#     args = parser.parse_args()

#     ConfigClass = ProductionConfig  # type: Type[Config]
#     RegistryClass = JsonJwtRegistry  # type: Type[Registry]

#     if args.developement:
#         ConfigClass = DevelopmentConfig
#         RegistryClass = MemoryRegistry

#     try:
#         config = ConfigClass()
#         registry = RegistryClass(config)
#         context = Context(config, registry)
#         gunicorn_config = config['gunicorn']
#     except Exception as e:
#         sys.exit("Configuration loading error: {0} {1}".format(type(e), e))

#     if args.terminal:
#         app = Main(context)
#         app.run()
#     else:
#         app = create_app(context)
#         Application(app, gunicorn_config).run()


import os
from .infrastructure.config import Config, build_config
from .infrastructure.resolver import Resolver
from .infrastructure.cli import Cli


def main():  # pragma: no cover
    mode = os.environ.get('AUTHARK_MODE', 'PROD')
    config_path = os.environ.get('AUTHARK_CONFIG', 'authark_config.json')
    config = build_config(config_path, mode)

    resolver = Resolver(config)
    providers = config['providers']
    registry = resolver.resolve(providers)

    Cli(config, registry)


if __name__ == '__main__':  # pragma: no cover
    main()
