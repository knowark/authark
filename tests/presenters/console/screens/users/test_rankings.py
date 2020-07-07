
import asyncio
from types import MethodType
from pytest import fixture, mark
from widark import Event
from authark.presenters.console.screens.users.rankings import (
    RankingsModal, RoleSelectionModal)

pytestmark = mark.asyncio


@fixture
def rankings_modal(root, injector):
    user = {'id': '1', 'name': 'John Doe'}
    return RankingsModal(root, injector=injector, user=user)


@fixture
def role_selection_modal(root, injector):
    return RoleSelectionModal(root, injector=injector)


async def test_rankings_instantiation_defaults(rankings_modal):
    assert rankings_modal.user == {'id': '1', 'name': 'John Doe'}


async def test_rankings_load(rankings_modal):
    rankings_modal.build()
    await rankings_modal.load()
    await asyncio.sleep(0)

    assert len(rankings_modal.body.data) == 1


async def test_rankings_on_modal_done(rankings_modal):
    role = {'id': '1', 'name': 'admin'}
    event = Event('Custom', 'done', details={'result': 'roles', 'role': role})
    assigned_role = None

    async def mock_assign_role(self, role_dict):
        nonlocal assigned_role
        assigned_role = role_dict

    rankings_modal.build()
    rankings_modal.management_manager.assign_role = MethodType(
        mock_assign_role, rankings_modal)
    await rankings_modal.on_modal_done(event)

    assert assigned_role == [{'role_id': '1', 'user_id': '1'}]
    assert rankings_modal.modal is None

    event = Event('Custom', 'done', details={'result': 'default'})
    await rankings_modal.on_modal_done(event)
    await asyncio.sleep(0)

    assert len(rankings_modal.body.data) == 1


async def test_rankings_on_assign(rankings_modal):
    event = Event('Mouse', 'click')
    await rankings_modal.on_assign(event)
    await asyncio.sleep(0)

    assert rankings_modal.modal is not None


async def test_rankings_on_body(rankings_modal):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_

            def focus(self):
                pass
        return MockTarget()

    deassigned_role = None

    async def mock_deassign_role(self, role_dict):
        nonlocal deassigned_role
        deassigned_role = role_dict

    rankings_modal.management_manager.deassign_role = MethodType(
        mock_deassign_role, rankings_modal)

    event = Event('Mouse', 'click')
    event.target = target(None)

    await rankings_modal.on_body(event)
    assert deassigned_role is None

    event.target = target({'id': '1',  'user_id': '1', 'role_id': '1'})
    event.button = 2

    await rankings_modal.on_body(event)
    await asyncio.sleep(0)

    assert deassigned_role == ['1']


async def test_role_selection_modal_load(role_selection_modal):
    role_selection_modal.build()
    await role_selection_modal.load()
    await asyncio.sleep(0)

    assert len(role_selection_modal.body.data) == 1


async def test_role_selection_modal_on_body(role_selection_modal):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    given_details = None

    async def mock_done(self, details):
        nonlocal given_details
        given_details = details

    role_selection_modal.done = MethodType(mock_done, role_selection_modal)

    event = Event('Mouse', 'click')
    event.target = target(None)

    await role_selection_modal.on_body(event)
    assert given_details is None

    event.target = target({'id': '1', 'name': 'admin'})

    await role_selection_modal.on_body(event)
    await asyncio.sleep(0)

    assert given_details == {
        'result': 'roles', 'role': {'id': '1', 'name': 'admin'}}
