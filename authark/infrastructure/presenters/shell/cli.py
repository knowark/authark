import logging
from argparse import ArgumentParser, Namespace
from injectark import Injectark
from typing import List, Dict
from ...core import Config
from .... import __version__
# from ..web import create_app, ServerApplication
# from ..terminal import Main, Context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Cli:
    def __init__(self, config: Config, injector: Injectark) -> None:
        self.config = config
        self.injector = injector
        self.registry = injector
        self.parser = ArgumentParser('Authark')

    async def run(self, argv: List[str]):
        namespace = await self.parse(argv)
        await namespace.func(vars(namespace))

    async def parse(self, argv: List[str]) -> Namespace:
        subparsers = self.parser.add_subparsers()

        # Provision
        provision_parser = subparsers.add_parser(
            'provision', help='Provision new tenants.')
        provision_parser.add_argument('name')
        provision_parser.set_defaults(func=self.provision)

        # Serve
        serve_parser = subparsers.add_parser(
            'serve', help='Start HTTP server.')
        serve_parser.set_defaults(func=self.serve)

        # Terminal
        # terminal_parser = subparsers.add_parser(
        #     'terminal', help='Open terminal interface.')
        # terminal_parser.set_defaults(func=self.terminal)

        # Load
        load_parser = subparsers.add_parser(
            'load', help='Load items from file.')
        load_parser.add_argument('input_file')
        load_parser.add_argument('-s', '--source')
        load_parser.add_argument('-p', '--password_field')
        load_parser.add_argument('-t', '--tenant')
        load_parser.set_defaults(func=self.load)

        # Version
        version_parser = subparsers.add_parser('version')
        version_parser.set_defaults(func=self.version)

        if len(argv) == 0:
            self.parser.print_help()
            self.parser.exit()

        return self.parser.parse_args(argv)

    async def provision(self, options_dict: Dict[str, str]) -> None:
        print('...PROVISION::::')
        tenant_supplier = self.injector['TenantSupplier']
        tenant_dict = {'name': options_dict['name']}
        tenant_supplier.create_tenant(tenant_dict)
        print('...END PROVISION::::')

    async def serve(self, options_dict: Dict[str, str]) -> None:
        print('...SERVE:::', options_dict)

        # print(create_app)
        # app = create_app(self.config, self.resolver)
        # ServerApplication(app, self.config['gunicorn']).run()

    async def terminal(self, options_dict: Dict[str, str]) -> None:
        print('...TERMINAL:::', options_dict)

        # context = Context(self.config, self.injector)

        terminal = self.injector['Terminal']
        terminal.run()

    async def load(self, options_dict: Dict[str, str]) -> None:
        print('::::::LOAD:::::', options_dict)
        input_file = options_dict.get('input_file')
        source = options_dict.get('source')
        if not source:
            source = 'erp.users'
        password_field = options_dict.get('password_field')
        if not password_field:
            password_field = 'password'
        tenant = options_dict.get('tenant')
        if not tenant:
            print('A tenant is required.')
            return

        tenant_supplier = self.injector.resolve('TenantSupplier')
        tenant_dict = next(
            iter(tenant_supplier.search_tenants(
                [('slug', '=', tenant)])), None)

        session_coordinator = self.injector.resolve('SessionCoordinator')
        session_coordinator.set_tenant(tenant_dict)

        import_coordinator = self.injector.resolve('ImportCoordinator')
        import_coordinator.import_users(input_file, source, password_field)

    async def version(self, options_dict: Dict[str, str]):
        logger.info('<< VERSION >>')
        logger.info(__version__)