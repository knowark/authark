import json
import logging
from argparse import ArgumentParser, Namespace
from injectark import Injectark
from typing import List, Dict
from ...core import Config
from ... import __version__
from ..rest import RestApplication
from ..console import ConsoleApplication
from .scheduler import Scheduler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Shell:
    def __init__(self, config: Config, injector: Injectark) -> None:
        self.config = config
        self.injector = injector
        self.parser = ArgumentParser('Authark')

    async def run(self, argv: List[str]):
        namespace = await self.parse(argv)
        await namespace.func(vars(namespace))

    async def parse(self, argv: List[str]) -> Namespace:
        subparsers = self.parser.add_subparsers()

        # Provision
        provision_parser = subparsers.add_parser(
            'provision', help='Provision new tenants.')
        provision_parser.add_argument('data', help='JSON encoded tenant.')
        provision_parser.set_defaults(func=self.provision)

        # Serve
        serve_parser = subparsers.add_parser(
            'serve', help='Start HTTP server.')
        serve_parser.add_argument('-p', '--port')
        serve_parser.set_defaults(func=self.serve)

        # Work
        work_parser = subparsers.add_parser(
            'work', help='Start background worker.')
        work_parser.set_defaults(func=self.work)

        # Console
        console_parser = subparsers.add_parser(
            'console', help='Open console interface.')
        console_parser.set_defaults(func=self.console)

        # Load
        load_parser = subparsers.add_parser(
            'load', help='Load items from file.')
        load_parser.add_argument('input_file')
        load_parser.add_argument('-t', '--tenant', required=True)
        load_parser.add_argument('-s', '--source')
        load_parser.add_argument('-p', '--password_field')
        load_parser.set_defaults(func=self.load)

        # Version
        version_parser = subparsers.add_parser('version')
        version_parser.set_defaults(func=self.version)

        if len(argv) == 0:
            self.parser.print_help()
            self.parser.exit()

        return self.parser.parse_args(argv)

    async def provision(self, options_dict: Dict[str, str]) -> None:
        logger.info('PROVISION')
        tenant_supplier = self.injector['TenantSupplier']
        tenant_dict = json.loads(options_dict['data'])
        logger.info("Creating tenant:", tenant_dict)
        tenant_supplier.create_tenant(tenant_dict)
        logger.info('END PROVISION')

    async def serve(self, options_dict: Dict[str, str]) -> None:
        logger.info('SERVE')
        port = int(options_dict.get('port') or self.config['port'])
        app = RestApplication(self.config, self.injector)
        await RestApplication.run(app, port)
        logger.info('END SERVE')

    async def work(self, options_dict: Dict[str, str]) -> None:
        logger.info('WORK')
        await Scheduler(self.injector).run(options_dict)
        logger.info('END WORK')

    async def console(self, options_dict: Dict[str, str]) -> None:
        logger.info('CONSOLE')
        app = ConsoleApplication(config=self.config, injector=self.injector)
        await app.run()

    async def load(self, options_dict: Dict[str, str]) -> None:
        logger.info('LOAD')
        input_file = options_dict['input_file']
        tenant = options_dict['tenant']
        source = options_dict.get('source', 'external')
        password_field = options_dict.get('password_field', 'password')

        tenant_supplier = self.injector['TenantSupplier']
        tenant_dict = tenant_supplier.resolve_tenant(tenant)

        session_manager = self.injector['SessionManager']
        session_manager.set_tenant(tenant_dict)

        import_manager = self.injector['ImportManager']
        await import_manager.import_users(input_file, source, password_field)

    async def version(self, options_dict: Dict[str, str]):
        logger.info('<< VERSION >>')
        logger.info(__version__)
