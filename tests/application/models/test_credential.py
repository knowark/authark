from authark.application.models.credential import Credential


def test_credential_creation() -> None:
    id_ = "1"
    user_id = "af1209fade"
    value = "e9cee71ab932fde863338d08be4de9dfe39ea049bdafb342ce659ec5450b69ae"
    client = "ANDROID_LG_0987"
    credential = Credential(id=id_, user_id=user_id, value=value,
                            client=client)

    assert credential.id == id_
    assert credential.user_id == user_id
    assert credential.type == 'password'
    assert credential.client == client
    assert credential.value == value
