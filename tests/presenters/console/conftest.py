import curses
from pytest import fixture
from widark.widget import Widget

from injectark import Injectark
from authark.core import DEVELOPMENT_CONFIG
from authark.factories import strategy_builder, factory_builder
from authark.presenters.console import ConsoleApplication


# @fixture
# def app():
#     config = DEVELOPMENT_CONFIG
#     strategy = strategy_builder.build(config['strategies'])
#     factory = factory_builder.build(config)

#     injector = Injectark(strategy, factory)

#     return ConsoleApplication(config=config, injector=injector)


import curses
from pytest import fixture
from widark.widget import Widget


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
def injector():
    config = DEVELOPMENT_CONFIG
    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    return Injectark(strategy, factory)
