import curses
from pytest import fixture
from widark.widget import Widget
from injectark import Injectark
from authark.integration.core import config as global_config
from authark.integration.factories import factory_builder
from authark.presentation.console import ConsoleApplication


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
    config = dict(global_config)
    config['factory'] = 'CheckFactory'
    config['strategies'] = ['base', 'check']
    return config


@fixture
def injector(config):
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    return Injectark(factory)
