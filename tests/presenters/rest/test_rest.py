import jwt
from json import loads, dumps
from authark.presenters.rest import RestApplication
from authark.presenters.rest import rest as rest_module


async def test_rest_application_run(monkeypatch):
    called = False
    app_called = False

    class web:
        @staticmethod
        async def _run_app(app, port=1234):
            nonlocal called
            called = True

    class MockRestApplication(RestApplication):
        def __init__(self) -> None:
            pass

        @property
        def app(self):
            nonlocal app_called
            app_called = True

    monkeypatch.setattr(rest_module, 'web', web)
    rest = MockRestApplication()

    await RestApplication.run(rest)

    assert called is True
    assert app_called is True


async def test_root(app) -> None:
    response = await app.get('/')

    content = await response.text()

    assert response.status == 200
    assert 'Authark' in content


async def test_root_api(app) -> None:
    response = await app.get('/?api')
    data = await response.text()
    api = loads(data)

    assert 'openapi' in api
    assert api['info']['title'] == 'Authark'


async def test_users_get_unauthorized(app) -> None:
    response = await app.get('/users')
    content = await response.text()

    assert response.status == 401
    data_dict = loads(content)
    assert 'error' in data_dict


async def test_users_head(app, headers) -> None:
    response = await app.head('/users', headers=headers)
    count = response.headers.get('Total-Count')

    assert response.status == 200
    assert int(count) == 2


async def test_get_users_filter(app, headers) -> None:
    response = await app.get(
        '/users?filter=[["id", "=", "1"]]', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)

    assert len(data_dict) == 1
    assert data_dict[0]['id'] == '1'


async def test_users_get(app, headers) -> None:
    response = await app.get('/users', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)

    assert len(data_dict) == 2
    assert data_dict[1]['id'] == '2'


async def test_users_register_put_route(app, headers) -> None:
    response = await app.put(
        '/users',
        data=dumps([dict(
            tenant="default",
            username="gecheverry",
            email="gecheverry@gmail.com",
            password="POI123"
        )]),
        headers=headers)

    assert response.status == 200

    response = await app.head('/users', headers=headers)
    count = response.headers.get('Total-Count')

    assert int(count) == 3


async def test_tokens_put_route_with_password(app):
    response = await app.put(
        '/tokens',
        data=dumps(dict(
            dominion="default",
            tenant="default",
            username="eecheverry",
            password="ABC1234"
        )))
    data = await response.text()
    assert response.status == 200
    assert len(data) > 0


async def xtest_tokens_put_route_with_refresh_token(app):
    token = jwt.encode(
        {'user': "pepe"}, 'REFRESHSECRET')
    response = await app.put(
        '/tokens',
        data=dumps(dict(
            dominion="default",
            tenant="default",
            refreshToken=token
        )))
    data = await response.text()
    assert response.status == 200
    assert len(data) > 0


async def test_registrations_put_route(app):
    response = await app.put(
        '/registrations',
        data=dumps(dict(
            organization="Knowark",
            username="eecheverry",
            email="eecheverry@knowark.com",
            password="ABC1234",
            name="Esteban Echeverry"
        )))
    data = await response.text()
    assert response.status == 200


async def test_verifications_put_route(app):
    token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWN0aXZhdG"
             "lvbiIsInRlbmFudCI6ImRlZmF1bHQiLCJ1c2VyX2lkIjoiMSJ9.DDsMjlYV"
             "I5U4AjTiAiSdQJPDEIH2y8R7HwvlO0oJuOs")
    response = await app.put(
        '/verifications',
        data=dumps(dict(
            tenant="default",
            token=token,
        )))
    data = await response.text()
    assert response.status == 200


async def test_registrations_enroll_put_route(app):
    response = await app.put(
        '/registrations',
        data=dumps(dict(
            organization="Default",
            username="masolano",
            email="masolano@knowark.com",
            password="XYZ1234",
            name="Miguel Alexis Solano",
            enroll=True
        )))
    data = await response.text()
    assert response.status == 200


async def test_users_delete(app, headers) -> None:
    response = await app.delete('/users/1', headers=headers)
    assert response.status == 204

    response = await app.get('/users', headers=headers)
    data_dict = loads(await response.text())

    assert len(data_dict) == 1


async def test_restrictions_delete(app, headers) -> None:
    response = await app.delete('/restrictions/1', headers=headers)
    assert response.status == 204

    response = await app.get('/restrictions', headers=headers)
    data_dict = loads(await response.text())

    assert len(data_dict) == 0


async def test_policies_delete(app, headers) -> None:
    response = await app.delete('/policies/1', headers=headers)
    assert response.status == 204

    response = await app.get('/policies', headers=headers)
    data_dict = loads(await response.text())

    assert len(data_dict) == 0


async def test_users_delete_body(app, headers) -> None:
    ids = dumps(["1"])
    response = await app.delete(
        '/users', data=ids, headers=headers)
    assert response.status == 204

    response = await app.get('/users', headers=headers)
    data_dict = loads(await response.text())

    assert len(data_dict) == 1


async def test_bad_filter_get_route_filter(app, headers) -> None:
    response = await app.get('/users?filter=[[**BAD FILTER**]]',
                             headers=headers)
    content = await response.text()
    data_dict = loads(content)
    assert len(data_dict) == 2


async def test_users_get_route_filter(app, headers) -> None:
    response = await app.get(
        '/users?filter=[["createdAt", "=", 9999999999]]',
        headers=headers)
    content = await response.text()
    data_dict = loads(content)
    assert len(data_dict) == 0


async def test_dominions_get(app, headers) -> None:
    response = await app.get('/dominions', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)

    assert len(data_dict) == 1
    assert data_dict[0]['name'] == 'default'


async def test_dominions_not_implemented_put(app, headers) -> None:
    response = await app.put(
        '/dominions',
        data=dumps(dict(
            name="cloudapp"
        )), headers=headers)
    content = await response.text()
    assert response.status == 500


async def test_dominions_not_implemented_delete(app, headers) -> None:
    response = await app.delete('/dominions/platform', headers=headers)
    content = await response.text()
    assert response.status == 500
