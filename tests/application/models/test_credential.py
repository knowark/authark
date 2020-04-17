from pytest import fixture
from authark.application.models import Credential


@fixture
def credential():
    return Credential(
        id='1',
        user_id='af1209fade',
        value='e9cee71ab932fde863338d08be4de9dfe39ea049bdafb342ce659ec5450b69ae',
        client='ANDROID_LG_0987'
    )


def test_credential_instantiation(credential):
    assert credential is not None


def test_credential_attributes(credential):
    assert credential.user_id == 'af1209fade'
    assert credential.type == 'password'
    assert credential.value == 'e9cee71ab932fde863338d08be4de9dfe39ea049bdafb342ce659ec5450b69ae'
    assert credential.client == 'ANDROID_LG_0987'

# def test_credential_creation():
#     id_ = "1"
#     user_id = "af1209fade"
#     value = "e9cee71ab932fde863338d08be4de9dfe39ea049bdafb342ce659ec5450b69ae"
#     client = "ANDROID_LG_0987"
#     credential = Credential(id=id_, user_id=user_id, value=value,
#                             client=client)

#     assert credential.id == id_
#     assert credential.user_id == user_id
#     assert credential.type == 'password'
#     assert credential.client == client
#     assert credential.value == value
