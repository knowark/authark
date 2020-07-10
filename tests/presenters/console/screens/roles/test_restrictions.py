
import asyncio
from types import MethodType
from pytest import fixture, mark
from widark import Event
from authark.presenters.console.screens.roles.restrictions import (
    RestrictionsModal,
    RestrictionDetailsModal
)

pytestmark = mark.asyncio


@fixture
def restrictions_modal(root, injector):
    policy = {'id': '1', 'resource': 'customers'}
    return RestrictionsModal(root, injector=injector, policy=policy)


@fixture
def restriction_details_modal(root, injector):
    restriction = {'id': '1', 'policy_id': '1', 'sequence': 0,
                   'name': 'Own Customers', 'target': 'customers',
                   'domain': '[["user_id", "=", ">>> user["id"]"]]'}
    return RestrictionDetailsModal(
        root, injector=injector, restriction=restriction)


async def test_restrictions_instantiation_defaults(restrictions_modal):
    assert restrictions_modal.policy == {'id': '1', 'resource': 'customers'}


async def test_restrictions_modal_load(restrictions_modal):
    restrictions_modal.build()
    await restrictions_modal.load()
    await asyncio.sleep(0)

    assert len(restrictions_modal.body.data) == 1


async def test_restrictions_modal_on_modal_done(restrictions_modal):
    event = Event('Custom', 'done', details={'result': 'default'})
    restrictions_modal.build()
    await restrictions_modal.on_modal_done(event)
    await asyncio.sleep(0)

    assert restrictions_modal.modal is None
    assert len(restrictions_modal.body.data) == 1


async def test_restrictions_screen_on_body(restrictions_modal):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    event = Event('Mouse', 'click')
    event.target = target(None)

    restrictions_modal.build()
    await restrictions_modal.on_body(event)
    assert restrictions_modal.modal is None

    event.target = target({
        'id': '', 'resource': '', 'privilege': '', 'active': ''})

    await restrictions_modal.on_body(event)
    await asyncio.sleep(0)

    assert restrictions_modal.modal is not None


async def test_restrictions_modal_on_create(restrictions_modal):
    event = Event('Mouse', 'click')
    await restrictions_modal.on_create(event)
    await asyncio.sleep(0)
    assert restrictions_modal.modal.restriction == {
        'id': '', 'policy_id': '1',  'name': '',
        'sequence': 0, 'target': 'customers', 'domain': ''}


async def test_restrictions_modal_on_cancel(restrictions_modal):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    restrictions_modal.done = MethodType(mock_done, restrictions_modal)

    await restrictions_modal.on_cancel(event)
    assert given_result == {'result': 'cancelled'}


async def test_restriction_details_modal_on_buttons(restriction_details_modal):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    restriction_details_modal.done = MethodType(
        mock_done, restriction_details_modal)

    await restriction_details_modal.on_cancel(event)
    assert given_result == {'result': 'cancelled'}

    await restriction_details_modal.on_delete(event)
    assert given_result == {'result': 'deleted'}


async def test_restriction_details_modal_on_save(restriction_details_modal):
    event = Event('Mouse', 'click')

    given_restrictions = None

    async def create_restriction(self, restrictions):
        nonlocal given_restrictions
        given_restrictions = restrictions

    restriction_details_modal.build()
    restriction_details_modal.security_manager.create_restriction = MethodType(
        create_restriction, restriction_details_modal)

    await restriction_details_modal.on_save(event)
    await asyncio.sleep(0)

    assert given_restrictions == [{
        'id': '1', 'policy_id': '1', 'sequence': 0,
        'name': 'Own Customers', 'target': 'customers',
        'domain': '[["user_id", "=", ">>> user["id"]"]]'}]
