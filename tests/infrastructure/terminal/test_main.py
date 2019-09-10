import urwid
from pytest import raises
from injectark import Injectark
from authark.infrastructure.terminal.main import Main
from authark.infrastructure.terminal.screens.main_menu import MainMenu
from authark.infrastructure.core import TrialConfig, build_factory
from authark.infrastructure.terminal.framework import Context


def test_main_instantiation(main):
    assert main is not None


def test_main_unhandled_input(main):
    assert main._unhandled_input('enter') is None
    with raises(urwid.ExitMainLoop):
        main._unhandled_input('meta q')


def test_main_run(main):
    called = False

    class MockLoop:
        def run(self):
            nonlocal called
            called = True
    main.loop = MockLoop()
    main.run()
    assert called


# def test_setup_initial_tenant_no_tenants():
#     config = TrialConfig()
#     factory = build_factory(config)
#     strategy = config['strategy']
#     resolver = Injectark(strategy=strategy, factory=factory)
#     context = Context(config, resolver)

#     main = Main(context)
#     main._setup_initial_tenant()
#     print("TENANT:::: ", main.session_coordinator.tenant_provider.state.tenant)
