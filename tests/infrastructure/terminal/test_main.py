import urwid
from pytest import raises
from authark.infrastructure.terminal.screens.main_menu import MainMenu


def test_main_instantiation(main):
    assert main is not None


def test_main_unhandled_input(main):
    with raises(urwid.ExitMainLoop):
        main._unhandled_input('ctrl c')


def test_main_run(main):
    called = False

    class MockLoop:
        def run(self):
            nonlocal called
            called = True
    main.loop = MockLoop()
    main.run()
    assert called
