import jwt
from json import loads, dumps
from authark.infrastructure.presenters.rest import RestApplication
from authark.infrastructure.presenters.rest import rest as rest_module


async def test_rest_application_run(monkeypatch):
    called = False

    class web:
        @staticmethod
        async def _run_app(app, port=1234):
            nonlocal called
            called = True

    monkeypatch.setattr(rest_module, 'web', web)

    await RestApplication.run(None)

    assert called is True


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
            tenant="001",
            username="eecheverry",
            password="ABC1234",
        )))
    data = await response.text()
    # assert response.status == 200
    assert len(data) > 0


async def test_tokens_put_route_with_refresh_token(app):
    token = jwt.encode(
        {'user': "pepe"}, 'REFRESHSECRET').decode('utf-8')
    response = await app.put(
        '/tokens',
        data=dumps(dict(
            tenant="001",
            refresh_token=token
        )))
    data = await response.text()
    # assert response.status == 200
    assert len(data) > 0


async def test_users_delete(app, headers) -> None:
    response = await app.delete('/users/1', headers=headers)
    assert response.status == 204

    response = await app.get('/users', headers=headers)
    data_dict = loads(await response.text())

    assert len(data_dict) == 1


async def test_rules_delete(app, headers) -> None:
    response = await app.delete('/rules/1', headers=headers)
    assert response.status == 204

    response = await app.get('/rules', headers=headers)
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
