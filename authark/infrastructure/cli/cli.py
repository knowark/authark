import sys
from argparse import ArgumentParser, Namespace
from ..config import Config
from ..resolver import Registry
from ..data import JsonArranger
from ..web import create_app, ServerApplication
from ..terminal import Main, Context


class Cli:
    def __init__(self, config: Config, registry: Registry) -> None:
        self.registry = registry
        self.config = config

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

        if len(sys.argv[1:]) == 0:
            parser.print_help()
            parser.exit()

        return parser.parse_args()

    def setup(self, args: Namespace) -> None:
        print('...SETUP:::', args)
        filename = self.config['database']['url']
        print('Filename:', filename)
        collections = [
            'users',
            'credentials',
            'dominions',
            'roles',
            'rankings'
        ]
        JsonArranger.make_json(filename, collections)

    def serve(self, args: Namespace) -> None:
        print('...SERVE:::', args)

        app = create_app(self.config, self.registry)
        gunicorn_config = self.config['gunicorn']
        ServerApplication(app, gunicorn_config).run()

    def terminal(self, args: Namespace) -> None:
        print('...TERMINAL:::', args)

        print('REGISTRY')
        print(self.registry)

        context = Context(self.config, self.registry)
        app = Main(context)
        app.run()
