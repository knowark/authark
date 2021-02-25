from inspect import signature
from authark.application.domain.services import (
    NotificationService, MemoryNotificationService)


def test_notification_service() -> None:
    methods = NotificationService.__abstractmethods__  # type: ignore
    assert 'notify' in methods

    sig = signature(NotificationService.notify)
    assert sig.parameters.get('content')


def test_memory_token_service_implementation() -> None:
    assert issubclass(MemoryNotificationService, NotificationService)


async def test_memory_notification_service_notify() -> None:
    content = {
        'to': "jdoe@mail.com",
        'subject': "Account activation",
        'message': 'Hello World!'}

    notification_service = MemoryNotificationService()
    await notification_service.notify(content)

    assert notification_service.content == content

