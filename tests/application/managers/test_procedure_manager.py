from authark.application.managers import ProcedureManager


def test_procedure_manager_creation(procedure_manager):
    assert hasattr(procedure_manager, 'fulfill')


async def test_procedure_manager_fulfill(procedure_manager):
    requisition_dict = {
        'type': 'reset',
        'tenant': 'default',
        'data':  {
            'email': 'gabeche@gmail.com'
        }
    }

    await procedure_manager.fulfill([requisition_dict])

    notification = procedure_manager.notification_service.notification

    assert notification == {
        'type': 'reset',
        'subject': 'Password Reset',
        'recipient': 'gabeche@gmail.com',
        'owner': 'Gabriel',
        'token': '{"type": "reset", "tenant": "default", "uid": "3"}'
    }


async def test_procedure_manager_register(procedure_manager):
    user_dicts = [{
        "id": "007",
        "name": "Miguel Vivas",
        "username": "mvp",
        "email": "mvp@gmail.com",
        "password": "PASS4"
    }]
    await procedure_manager.register(user_dicts)
    credential_repository = (
        procedure_manager.enrollment_service.credential_repository)
    user_repository = procedure_manager.user_repository
    notification_service = procedure_manager.notification_service

    assert len(user_repository.data['default']) == 4
    [new_user] = await user_repository.search([('id', '=', '007')])
    assert new_user.username == 'mvp'
    assert new_user.active is False

    assert len(credential_repository.data['default']) == 4
    assert notification_service.notification == {
        'type': 'activation',
        'subject': 'Account Activation',
        'recipient': 'mvp@gmail.com',
        'owner': 'Miguel Vivas',
        'token': (
            '{"type": "activation", "tenant": "default", "uid": "007"}')
    }


async def test_procedure_manager_verify_activation(procedure_manager):
    verification_dicts: RecordList = [{
        "tenant": "default",
        'token': '{"type": "activation", "tenant": "default", "uid": "1"}'
    }]

    user_repository = procedure_manager.user_repository

    await procedure_manager.verify(verification_dicts)

    [user] = await user_repository.search([('id', '=', '1')])

    assert user.active is True


async def test_procedure_manager_verify_reset(procedure_manager):
    verification_dicts: RecordList = [{
        "tenant": "default",
        'token': '{"type": "reset", "tenant": "default", "uid": "1"}',
        'data': {'password': 'NEW_PASSWORD'}
    }]

    await procedure_manager.verify(verification_dicts)

    user_repository = procedure_manager.user_repository
    credential_repository = (
        procedure_manager.enrollment_service.credential_repository)

    [user] = await user_repository.search([('id', '=', '1')])
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

    await procedure_manager.update(user_dicts)
    credential_repository = (
        procedure_manager.enrollment_service.credential_repository)
    user_repository = procedure_manager.user_repository

    assert len(user_repository.data['default']) == 3
    assert len(credential_repository.data['default']) == 3
    assert user_repository.data['default']['1'].username == "valenep"
    assert "HASHED: NEW: PASS1" in [
        credential.value for credential in
        credential_repository.data['default'].values()]


# async def test_auth_manager_update_without_password(auth_manager):
    # user_dicts: RecordList = [{
        # "id": "1",
        # "username": "valenep",
        # "email": "valenep@outlook.com",
    # }]

    # await auth_manager.update(user_dicts)
    # credential_repository = auth_manager.credential_repository
    # user_repository = auth_manager.user_repository

    # assert len(user_repository.data['default']) == 3
    # assert len(credential_repository.data['default']) == 3
    # assert user_repository.data['default']['1'].username == "valenep"
    # assert user_repository.data['default']['1'].email == "valenep@outlook.com"
