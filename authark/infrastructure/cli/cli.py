import sys
from argparse import ArgumentParser, Namespace
from injectark import Injectark
from ..config import Config
from ..data import JsonArranger
from ..web import create_app, ServerApplication
from ..terminal import Main, Context


class Cli:
    def __init__(self, config: Config, resolver: Injectark) -> None:
        self.config = config
        self.resolver = resolver

        args = self.parse()
        args.func(args)

    def parse(self) -> Namespace:
        parser = ArgumentParser('Authark')
        subparsers = parser.add_subparsers()

        # Setup
        setup_parser = subparsers.add_parser('setup')
        setup_parser.set_defaults(func=self.setup)

        # Serve
        serve_parser = subparsers.add_parser('serve')
        serve_parser.set_defaults(func=self.serve)

        # Terminal
        terminal_parser = subparsers.add_parser('terminal')
        terminal_parser.set_defaults(func=self.terminal)

        # Load
        load_parser = subparsers.add_parser('load')
        load_parser.add_argument('input_file')
        load_parser.add_argument('-s', '--source')
        load_parser.add_argument('-p', '--password_field')
        load_parser.set_defaults(func=self.load)

        if len(sys.argv[1:]) == 0:
            parser.print_help()
            parser.exit()

        return parser.parse_args()

    # def setup(self, args: Namespace) -> None:
    #     print('...SETUP:::', args)
    #     filename = self.config['database']['url']
    #     print('Filename:', filename)
    #     collections = [
    #         'users',
    #         'credentials',
    #         'dominions',
    #         'roles',
    #         'rankings',
    #         'policies',
    #         'permissions',
    #         'resources',
    #         'grants'
    #     ]
    #     JsonArranger.make_json(filename, collections)

    def setup(self, args: Namespace) -> None:
        print('...SETUP:::', args)
        setup_coordinator = self.resolver.resolve('SetupCoordinator')
        setup_coordinator.setup_server()

    def serve(self, args: Namespace) -> None:
        print('...SERVE:::', args)

        app = create_app(self.config, self.resolver)
        gunicorn_config = self.config['gunicorn']
        ServerApplication(app, gunicorn_config).run()

    def terminal(self, args: Namespace) -> None:
        print('...TERMINAL:::', args)

        context = Context(self.config, self.resolver)
        app = Main(context)
        app.run()

    def load(self, args: Namespace) -> None:
        print('::::::LOAD:::::', args.input_file)
        input_file = args.input_file
        source = args.source
        if not source:
            source = 'erp.users'
        password_field = args.password_field
        if not password_field:
            password_field = 'password'
        import_coordinator = self.resolver.resolve('ImportCoordinator')
        import_coordinator.import_users(input_file, source, password_field)
