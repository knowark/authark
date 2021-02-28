from pytest import fixture
from email.message import EmailMessage
from authark.core.suppliers import MemoryTemplateSupplier
from authark.core.mail import MailNotificationService
from authark.core.mail import (
    mail_notification_service as mail_notification_service_module)



@fixture
def mail_notification_service():
    template_supplier = MemoryTemplateSupplier()
    return MailNotificationService(
        {'sender': 'admin@mail.com', 'host': 'smtp.knowark.com',
         'port': 587, 'username': 'infobot', 'password': 'pass123',
         'url': 'http://api.tempos.local/rest/auth'},
        template_supplier)


def test_mail_notification_service_instantiation(mail_notification_service):
    assert isinstance(mail_notification_service, MailNotificationService)


async def test_mail_notification_service_notify(
    monkeypatch, mail_notification_service):

    send_content = {}

    async def mock_send(message, hostname, port, username, password, use_tls):
        nonlocal send_content
        send_content['message'] = message
        send_content['hostname'] = hostname
        send_content['port'] = port
        send_content['username'] = username
        send_content['password'] = password

    monkeypatch.setattr(mail_notification_service_module, 'send', mock_send)

    content = {
        'type': 'activation',
        'subject': 'New Account Activation',
        'recipient': 'valenep@example.com',
        'owner': 'Valentina',
        'token': '<verification_token>'
    }

    await mail_notification_service.notify(content)

    assert isinstance(send_content['message'], EmailMessage)
    assert send_content['message']['From'] == 'admin@mail.com'
    assert send_content['message']['To'] == 'valenep@example.com'
    assert send_content['message']['Subject'] == 'New Account Activation'
    assert send_content['message'].get_content() == (
        "activation.html: {'url': 'http://api.tempos.local/rest/auth', "
        "'type': 'activation', 'subject': 'New Account Activation', "
        "'recipient': 'valenep@example.com', 'owner': 'Valentina', "
        "'token': '<verification_token>'}\n"
    )
    assert send_content['hostname'] == 'smtp.knowark.com'
    assert send_content['port'] == 587
    assert send_content['username'] == 'infobot'
    assert send_content['password'] == 'pass123'
