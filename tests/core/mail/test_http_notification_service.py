import asyncio
from pytest import fixture
from unittest.mock import MagicMock, AsyncMock
from aiohttp import ClientSession
from authark.core.mail import HttpNotificationService
from authark.core.mail import (
    http_notification_service as http_notification_service_module)


@fixture
def http_notification_service():
    config = {'url': 'https://mediak.knowark.com/emails'}
    return HttpNotificationService(config)


def test_http_notification_service_instantiation(http_notification_service):
    assert isinstance(http_notification_service, HttpNotificationService)


async def test_http_notification_service_notify(
    monkeypatch, http_notification_service):

    MockClientSession = MagicMock(ClientSession, autospec=True)
    MockClientSession.close = AsyncMock()

    monkeypatch.setattr(
        http_notification_service_module, 'ClientSession', MockClientSession)

    content = {
        'type': 'activation',
        'subject': 'New Account Activation',
        'recipient': 'valenep@example.com',
        'owner': 'Valentina',
        'token': '<verification_token>'
    }

    await http_notification_service.notify(content)

    session = http_notification_service.session

    session.patch.assert_called_once()
    session.patch.assert_called_once_with(
        'https://mediak.knowark.com/emails', json={
            'meta': {}, 'data': {
                'recipient': 'valenep@example.com',
                'context':  content
            }
        })
