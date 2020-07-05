
import asyncio
from types import MethodType
from pytest import fixture, mark
from widark import Event
from authark.presenters.console.screens.dominions.policies import (
    PoliciesModal, PolicyDetailsModal)

pytestmark = mark.asyncio


@fixture
def policies_modal(root, injector):
    role = {'id': '1', 'name': 'admin'}
    return PoliciesModal(root, injector=injector, role=role)


@fixture
def policy_details_modal(root, injector):
    policy = {'id': '1', 'active': False, 'privilege': '',
              'resource': '', 'role_id': '1'}
    return PolicyDetailsModal(root, injector=injector, policy=policy)


async def test_policies_instantiation_defaults(policies_modal):
    assert policies_modal.role == {'id': '1', 'name': 'admin'}


async def test_policies_modal_load(policies_modal):
    await policies_modal.load()
    await asyncio.sleep(0)

    assert len(policies_modal.body.data) == 1


async def test_policies_modal_on_modal_done(policies_modal):
    event = Event('Custom', 'done', details={'result': 'default'})
    await policies_modal.on_modal_done(event)
    await asyncio.sleep(0)

    assert policies_modal.modal is None
    assert len(policies_modal.body.data) == 1


async def test_policies_screen_on_body(policies_modal):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    event = Event('Mouse', 'click')
    event.target = target(None)

    await policies_modal.on_body(event)
    assert policies_modal.modal is None

    event.target = target({
        'id': '', 'resource': '', 'privilege': '', 'active': ''})

    await policies_modal.on_body(event)
    await asyncio.sleep(0)

    assert policies_modal.modal is not None


async def test_policies_modal_on_create(policies_modal):
    event = Event('Mouse', 'click')
    await policies_modal.on_create(event)
    await asyncio.sleep(0)
    assert policies_modal.modal.policy == {
        'active': False, 'id': '', 'privilege': '',
        'resource': '', 'role_id': '1'}


async def test_policies_modal_on_cancel(policies_modal):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    policies_modal.done = MethodType(mock_done, policies_modal)

    await policies_modal.on_cancel(event)
    assert given_result == {'result': 'cancelled'}


async def test_policy_details_modal_on_buttons(policy_details_modal):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    policy_details_modal.done = MethodType(mock_done, policy_details_modal)

    await policy_details_modal.on_cancel(event)
    assert given_result == {'result': 'cancelled'}

    await policy_details_modal.on_delete(event)
    assert given_result == {'result': 'deleted'}


async def test_policy_details_modal_on_save(policy_details_modal):
    event = Event('Mouse', 'click')

    given_policies = None

    async def create_policy(self, policies):
        nonlocal given_policies
        given_policies = policies

    policy_details_modal.security_manager.create_policy = MethodType(
        create_policy, policy_details_modal)

    await policy_details_modal.on_save(event)
    await asyncio.sleep(0)

    assert given_policies == [
        {'active': False, 'id': '1', 'privilege': '',
         'resource': '', 'role_id': '1'}]
