
import asyncio
from types import MethodType
from pytest import fixture, mark
from widark import Event
from authark.presenters.console.screens.dominions.dominions import (
    DominionsScreen, DominionDetailsModal)

pytestmark = mark.asyncio


@fixture
def dominions_screen(root, injector):
    return DominionsScreen(root, injector=injector)


@fixture
def dominion_details_modal(root, injector):
    dominion = {'id': '1', 'name': 'Proser', 'url': ''}
    return DominionDetailsModal(root, injector=injector, dominion=dominion)


async def test_dominions_screen_instantiation_defaults(dominions_screen):
    assert dominions_screen.dominion is None


async def test_dominions_screen_load(dominions_screen):
    await dominions_screen.load()
    await asyncio.sleep(0)

    assert len(dominions_screen.body.data) == 1


async def test_dominions_screen_on_body(dominions_screen):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    event = Event('Mouse', 'click')
    event.target = target(None)

    await dominions_screen.on_body(event)
    assert dominions_screen.modal is None

    event.target = target({'name': '', 'url': ''})

    await dominions_screen.on_body(event)
    await asyncio.sleep(0)

    assert dominions_screen.modal is not None


async def test_dominions_screen_on_create(dominions_screen):
    event = Event('Mouse', 'click')
    await dominions_screen.on_create(event)
    await asyncio.sleep(0)
    assert dominions_screen.modal.dominion == {'name': '', 'url': ''}


async def test_dominions_screen_on_modal_done(dominions_screen):
    dominions_screen.dominion = {'id': '1', 'name': 'Proser', 'url': ''}
    event = Event('Custom', 'done', details={'result': 'other'})
    await dominions_screen.on_modal_done(event)
    await asyncio.sleep(0)

    assert len(dominions_screen.body.data) == 1


async def test_dominions_screen_on_backdrop_click(dominions_screen):
    event = Event('Mouse', 'click')

    await dominions_screen.on_backdrop_click(event)
    assert dominions_screen.modal is None

    removed = None

    def mock_remove(self, widget):
        nonlocal removed
        removed = widget

    dominions_screen.remove = MethodType(mock_remove, dominions_screen)

    class MockModal:
        def hit(self, event):
            return False

    mock_modal = MockModal()
    dominions_screen.modal = mock_modal

    await dominions_screen.on_backdrop_click(event)
    await asyncio.sleep(0)

    assert dominions_screen.modal is None
    assert removed is mock_modal


async def test_dominions_details_modal_on_save(dominion_details_modal):
    event = Event('Mouse', 'click')

    given_dominions = None

    async def mock_update(self, dominions):
        nonlocal given_dominions
        given_dominions = dominions

    dominion_details_modal.build()
    dominion_details_modal.management_manager.create_dominion = MethodType(
        mock_update, dominion_details_modal)

    await dominion_details_modal.on_save(event)
    await asyncio.sleep(0)

    assert given_dominions == [{'id': '1', 'name': 'Proser', 'url': ''}]


async def test_dominions_details_modal_on_buttons(dominion_details_modal):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    dominion_details_modal.done = MethodType(mock_done, dominion_details_modal)

    await dominion_details_modal.on_cancel(event)
    assert given_result == {'result': 'cancelled'}

    await dominion_details_modal.on_delete(event)
    assert given_result == {'result': 'deleted'}

    await dominion_details_modal.on_roles(event)
    assert given_result == {'result': 'roles'}
