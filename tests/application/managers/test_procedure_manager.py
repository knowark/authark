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

async def test_procedure_manager_verify(procedure_manager):
    verification_dicts: RecordList = [{
        "tenant": "default",
        'token': '{"type": "activation", "tenant": "default", "uid": "1"}'
    }]

    await procedure_manager.verify(verification_dicts)

    user_repository = procedure_manager.user_repository

    [user] = await user_repository.search([('id', '=', '1')])

    assert user.active is True
