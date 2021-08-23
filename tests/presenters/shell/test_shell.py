
import json
from typing import List
from pytest import raises
from authark.presenters.shell import shell as shell_module


def test_shell_instantiation(shell):
    assert shell is not None


async def test_shell_run(shell):
    called = False

    class MockArgs:
        async def func(self, args):
            self.args = args

    async def mock_parse(argv: List[str]):
        nonlocal called
        called = True
        return MockArgs()

    shell.parse = mock_parse
    argv: List = []
    await shell.run(argv)

    assert called is True


async def test_shell_parse(shell):
    argv = ['version']
    result = await shell.parse(argv)

    assert result is not None


async def test_shell_parse_empty_argv(shell):
    shell.parser.print_help = lambda: None
    with raises(SystemExit) as e:
        await shell.parse([])


async def test_shell_version(shell):
    options_dict = {}
    assert await shell.version(options_dict) is None


async def test_shell_serve(shell, monkeypatch):
    called = False
    custom_port = None

    class MockRestApplication:
        def __init__(self, config, injector):
            pass

        @staticmethod
        async def run(app, port):
            nonlocal called, custom_port
            called = True
            custom_port = port

    monkeypatch.setattr(
        shell_module, 'RestApplication', MockRestApplication)

    await shell.serve({
        'port': '9201'
    })

    assert called and called
    assert custom_port == 9201


async def test_shell_provision(shell):
    options_dict = {
        'data': json.dumps({
            'name': 'Knowark'
        })
    }

    result = await shell.provision(options_dict)

    assert result is None


async def test_shell_console(shell, monkeypatch):
    called = False

    class MockConsoleApplication:
        def __init__(self, config, injector):
            pass

        async def run(self):
            nonlocal called
            called = True

    monkeypatch.setattr(
        shell_module, 'ConsoleApplication', MockConsoleApplication)

    await shell.console({})

    assert called and called


async def test_shell_load(shell, monkeypatch):
    options_dict = {
        'input_file': "external_users.json",
        'tenant': "default",
    }

    users_file = None
    default_source = None
    default_password_field = None

    async def mock_import_users(filepath: str, source: str,
                                password_field: str):
        nonlocal users_file, default_source, default_password_field
        users_file = filepath
        default_source = source
        default_password_field = password_field

    import_manager = shell.injector['ImportManager']
    import_manager.import_users = mock_import_users

    await shell.load(options_dict)

    assert users_file == 'external_users.json'
    assert default_source == 'external'
    assert default_password_field == 'password'


async def test_shell_work(shell, monkeypatch):
    given_options = None

    class MockScheduler:
        def __init__(self, injector):
            pass

        async def run(self, options):
            nonlocal given_options
            given_options = options

    monkeypatch.setattr(
        shell_module, 'Scheduler', MockScheduler)

    await shell.work({})

    assert given_options == {}


async def test_shell_time(shell, monkeypatch):
    given_options = None

    class MockScheduler:
        def __init__(self, injector):
            pass

        async def run(self, options):
            nonlocal given_options
            given_options = options

    monkeypatch.setattr(
        shell_module, 'Scheduler', MockScheduler)

    await shell.time({})

    assert given_options == {'time': True}
