import curses
from pytest import fixture
from widark.widget import Widget
from injectark import Injectark
from authark.core import DEVELOPMENT_CONFIG
from authark.factories import strategy_builder, factory_builder
from authark.presenters.console import ConsoleApplication


@fixture
def stdscr():
    stdscr = curses.initscr()
    curses.start_color()

    yield stdscr

    try:
        curses.endwin()
    except curses.error:
        pass


@fixture
def root(stdscr):
    root = Widget(None)
    # Run all tests with a resolution
    # of 18 rows and 90 cols
    stdscr.resize(18, 90)
    root.window = stdscr
    return


@fixture
def config():
    return DEVELOPMENT_CONFIG


@fixture
def injector(config):
    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    return Injectark(strategy, factory)
