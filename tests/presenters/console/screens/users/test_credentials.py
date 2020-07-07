
import asyncio
from pytest import fixture, mark
from authark.presenters.console.screens.users.credentials import (
    CredentialsModal)

pytestmark = mark.asyncio


@fixture
def credentials_modal(root, injector):
    user = {'id': '1', 'name': 'John Doe'}
    return CredentialsModal(root, injector=injector, user=user)


async def test_credentials_instantiation_defaults(credentials_modal):
    assert credentials_modal.user == {'id': '1', 'name': 'John Doe'}


async def test_credentials_load(credentials_modal):
    credentials_modal.build()
    await credentials_modal.load()

    await asyncio.sleep(0)

    assert len(credentials_modal.body.data) == 2
