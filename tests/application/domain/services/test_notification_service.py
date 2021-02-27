from inspect import signature
from pytest import raises
from authark.application.domain.common import NotificationError
from authark.application.domain.services import (
    NotificationService, MemoryNotificationService)


def test_notification_service() -> None:
    methods = NotificationService.__abstractmethods__  # type: ignore
    assert 'notify' in methods

    sig = signature(NotificationService.notify)
    assert sig.parameters.get('notification')


def test_memory_token_service_implementation() -> None:
    assert issubclass(MemoryNotificationService, NotificationService)


async def test_memory_notification_service_notify() -> None:
    notification = {
        'type': 'activation',
        'to': "jdoe@mail.com",
        'subject': "Account activation",
        'message': 'Hello World!'}

    notification_service = MemoryNotificationService()
    await notification_service.notify(notification)

    assert notification_service.notification == notification

async def test_memory_notification_service_notify_unknown() -> None:
    notification = {
        'type': 'unknown',
        'to': "jdoe@mail.com",
        'subject': "Account activation",
        'message': 'Hello World!'}

    notification_service = MemoryNotificationService()

    with raises(NotificationError):
        await notification_service.notify(notification)
