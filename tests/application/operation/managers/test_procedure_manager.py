from pytest import fixture, raises
from authark.application.domain.common import  EmailExistsError
from authark.application.domain.models import User, Credential
from authark.application.operation.managers import ProcedureManager


def test_procedure_manager_creation(procedure_manager):
    assert hasattr(procedure_manager, 'fulfill')


async def test_procedure_manager_fulfill_not_tenant(procedure_manager):
    requisition_dict = {
        'type': 'reset',
        'data':  {
            'email': 'gabeche2@gmail.com'
        }
    }
    plan_supplier = procedure_manager.plan_supplier

    with raises(EmailExistsError):
        await procedure_manager.fulfill({
            "meta": {},
            "data": [requisition_dict]
        })

async def test_procedure_manager_fulfill(procedure_manager):
    requisition_dict = {
        'type': 'reset',
        'data':  {
            'email': 'gabeche@gmail.com'
        }
    }
    plan_supplier = procedure_manager.plan_supplier

    await procedure_manager.fulfill({
        "meta": {},
        "data": [requisition_dict]
    })

    assert plan_supplier._notify_calls[0].__class__.__name__ == (
        'PasswordReset')
    assert vars(plan_supplier._notify_calls[0]) == {
        'type': 'reset',
        'subject': 'Password Reset',
        'template': 'mail/auth/reset_pasword.html',
        'recipient': 'gabeche@gmail.com',
        'owner': 'gabeche',
        'authorization': (
            '{"type": "authorization", "tenant": "anonymous",'
            ' "tid": "", "uid": "", "name": "", "email": ""}'),
        'context': {
                 'multiple_links':(
                     '<a href="http://dash.example.local/login/'
                     'reset?verification_token={"type": "reset", '
                     '"tenant": "default", "tid": "001", "temail": '
                     '"gabeche@gmail.com"}">Default</a><br>'),
                 'unsubscribe_link': 'unsubscribe_link.com',
                 'user_name': 'gabeche',
             }
         }


async def test_procedure_manager_register(procedure_manager):
    user_dicts = {
        "id": "007",
        "organization": "Manzanar",
        "name": "Miguel Vivas",
        "username": "mvp",
        "email": "mvp@gmail.com",
        "password": "PASS4"
    }
    await procedure_manager.register({
        "meta": {},
        "data": user_dicts
    })
    credential_repository = (
        procedure_manager.enrollment_service.credential_repository)
    user_repository = procedure_manager.user_repository
    plan_supplier = procedure_manager.plan_supplier

    assert len(user_repository.data['manzanar']) == 1
    [new_user] = await user_repository.search([('id', '=', '007')])
    assert new_user.username == 'mvp'
    assert new_user.active is False

    assert len(credential_repository.data['manzanar']) == 2
    assert len(plan_supplier._notify_calls) == 1
    assert plan_supplier._notify_calls[0].__class__.__name__ == (
        'UserRegistered')
    assert vars(plan_supplier._notify_calls[0])['owner'] == 'Miguel Vivas'
    assert vars(plan_supplier._notify_calls[0])['recipient'] == (
        'mvp@gmail.com')
    assert vars(plan_supplier._notify_calls[0])['subject'] == (
        'Account Activation')
    assert vars(plan_supplier._notify_calls[0])['type'] == (
        'activation')


async def test_procedure_manager_verify_activation(procedure_manager):
    verification_dicts: RecordList = [{
        "tenant": "default",
        'token': ('{"type": "activation",'
                  ' "tenant": "default",'
                  ' "uid": "3", "temail": "gabeche@gmail.com"}')
    }]
    user_repository = procedure_manager.user_repository

    result =  await procedure_manager.verify({
        "meta": {},
        "data": verification_dicts
    })

    [user] = await user_repository.search([('id', '=', '3')])
    assert user.active is True


async def test_procedure_manager_verify_reset(procedure_manager):
    verification_dicts: RecordList = [{
        "tenant": "default",
        'token': ('{"type": "reset", '
                  '"tenant": "default",'
                  ' "uid": "3", "temail": "gabeche@gmail.com"}'),
        'data': {'password': 'NEW_PASSWORD'}
    }]
    user_repository = procedure_manager.user_repository
    credential_repository = (
        procedure_manager.enrollment_service.credential_repository)

    await procedure_manager.verify({
        "meta": {},
        "data": verification_dicts
    })

    [user] = await user_repository.search([('id', '=', '3')])
    [credential] = await credential_repository.search(
        [('user_id', '=', user.id)])
    assert credential.value == 'HASHED: NEW_PASSWORD'


async def test_procedure_manager_update(procedure_manager) -> None:
    user_dicts = [{
        "id": "1",
        "username": "valenep",
        "email": "valenep@gmail.com",
        "password": "NEW: PASS1"
    }]

    await procedure_manager.update(dict(meta={}, data=user_dicts))
    credential_repository = (
        procedure_manager.enrollment_service.credential_repository)
    user_repository = procedure_manager.user_repository

    assert len(user_repository.data['default']) == 3
    assert len(credential_repository.data['default']) == 4
    assert user_repository.data['default']['1'].username == "valenep"
    assert "HASHED: NEW: PASS1" in [
        credential.value for credential in
        credential_repository.data['default'].values()]


async def test_procedure_manager_identity_provider_register(procedure_manager):
    user_dicts = {
        "organization": "Wonderland",
        "email": "facebook@provider.oauth",
        "username": "",
        "password": "AUTHORIZATION_CODE_XYZ1234"
    }
    procedure_manager.identity_service.user = User(
        email="alice@outlook.com", name="Alice Wonder")

    await procedure_manager.register({
        "meta": {},
        "data": user_dicts
    })
    credential_repository = (
        procedure_manager.enrollment_service.credential_repository)
    user_repository = procedure_manager.user_repository

    assert len(user_repository.data['wonderland']) == 2
    [new_user] = await user_repository.search([
        ('name', '=', 'Alice Wonder')])
    assert new_user.email == 'alice@outlook.com'
    assert new_user.active is False


async def test_procedure_manager_deregister(procedure_manager):
    user_repository = procedure_manager.user_repository
    user_ids = [user.id for user in await user_repository.search(
        [('id', '=', '2')])]

    unregistered = await procedure_manager.deregister({
        "meta": {},
        "data": user_ids
    })

    assert len(user_repository.data['default']) == 2

async def test_procedure_manager_register_not_dominion(procedure_manager):

    dominion = (await procedure_manager._ensure_dominion('default'))

    assert 'default' in dominion.name

async def test_auth_manager_refresh_register_refresh_token_not_found(
        procedure_manager):
    refresh_token = await procedure_manager._generate_refresh_token(
        '4', 'tempos')

    credential_repository = procedure_manager.credential_repository

    assert isinstance(refresh_token, str)
    assert len(credential_repository.data['default']) == 4
