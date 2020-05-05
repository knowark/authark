import contextlib
from typing import List
from pytest import raises
from unittest.mock import Mock, call
from authark.infrastructure.cli import cli as cli_module
from authark.infrastructure.cli import Cli
from io import StringIO


def test_cli_instantiation(cli):
    assert cli is not None


async def test_cli_run(cli):
    called = False

    class MockArgs:
        async def func(self, args):
            self.args = args

    async def mock_parse(argv: List[str]):
        nonlocal called
        called = True
        return MockArgs()

    cli.parse = mock_parse
    argv: List = []
    await cli.run(argv)

    assert called is True


async def test_cli_parse(cli):
    argv = ['version']
    result = await cli.parse(argv)

    assert result is not None


async def test_cli_parse_empty_argv(cli):
    cli.parser.print_help = lambda: None
    with raises(SystemExit) as e:
        await cli.parse([])


async def test_cli_version(cli):
    options_dict = {}
    assert await cli.version(options_dict) is None


async def test_cli_provision(cli, monkeypatch):
    options_dict = {"name": "custom"}

    await cli.provision(options_dict)
    tenants = cli.injector["TenantSupplier"].provider.search_tenants("")

    assert len(tenants) == 1
    assert tenants[0]["name"] == "custom"


# def test_cli_serve(cli, monkeypatch, namespace):
#     called = False

#     class MockServerApplication:
#         def __init__(self, app, options):
#             pass

#         def run(self):
#             nonlocal called
#             called = True

#     create_app_called = False

#     def mock_create_app_function(config, resolver):
#         nonlocal create_app_called
#         create_app_called = True

#     monkeypatch.setattr(
#         cli_module, 'ServerApplication', MockServerApplication)
#     monkeypatch.setattr(
#         cli_module, 'create_app', mock_create_app_function)

#     cli.serve(namespace)

#     assert called and create_app_called


# def test_cli_terminal(cli, monkeypatch, namespace):
#     called = False

#     class MockTerminalMain:
#         def __init__(self, context):
#             pass

#         def run(self):
#             nonlocal called
#             called = True

#     monkeypatch.setattr(cli_module, 'Main', MockTerminalMain)

#     cli.terminal(namespace)

#     assert called


# def test_cli_load(cli, monkeypatch, namespace):
#     namespace.input_file = ""
#     namespace.source = ""
#     namespace.password_field = ""
#     namespace.tenant = "servagro"
#     namespace.name = "servagro"

#     cli.provision(namespace)

#     temp_stdout = StringIO()
#     with contextlib.redirect_stdout(temp_stdout):
#         cli.load(namespace)

#     output = temp_stdout.getvalue().strip()
#     assert output == '::::::LOAD:::::'

#     # With source and password
#     namespace.source = "source"
#     namespace.password_field = "my_password"
#     temp_stdout = StringIO()
#     with contextlib.redirect_stdout(temp_stdout):
#         cli.load(namespace)

#     output = temp_stdout.getvalue().strip()
#     assert output == '::::::LOAD:::::'


# def test_cli_load_no_tentant_setted(cli, monkeypatch, namespace):
#     namespace.input_file = ""
#     namespace.source = ""
#     namespace.password_field = ""
#     namespace.tenant = ""

#     temp_stdout = StringIO()
#     with contextlib.redirect_stdout(temp_stdout):
#         cli.load(namespace)

#     output = temp_stdout.getvalue().strip()
#     assert output == '::::::LOAD::::: \nA tenant is required.'
