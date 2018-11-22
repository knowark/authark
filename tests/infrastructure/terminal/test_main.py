import urwid
from pytest import raises
from authark.infrastructure.terminal.screens.main_menu import MainMenu


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
