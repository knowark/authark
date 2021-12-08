import jwt
from json import loads, dumps
from authark.presentation.platform.rest import RestApplication
from authark.presentation.platform.rest import rest as rest_module


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
    assert 'errors' in data_dict


async def test_users_head(app, headers) -> None:
    response = await app.head('/users', headers=headers)
    count = response.headers.get('Count')

    assert response.status == 200
    assert int(count) == 2


async def test_get_users_filter(app, headers) -> None:
    response = await app.get(
        '/users?filter=[["id", "=", "1"]]', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)['data']

    assert len(data_dict) == 1
    assert data_dict[0]['id'] == '1'


async def test_users_get(app, headers) -> None:
    response = await app.get('/users', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)['data']

    assert len(data_dict) == 2
    assert data_dict[1]['id'] == '2'


async def test_users_register_patch_route(app, headers) -> None:
    response = await app.patch(
        '/users',
        data=dumps({
            "data":[{
                "tenant":"default",
                "username":"gecheverry",
                "email":"gecheverry@gmail.com",
                "password":"POI123"
            }]
        }),
        headers=headers)

    assert response.status == 200

    response = await app.head('/users', headers=headers)
    count = response.headers.get('Count')

    assert int(count) == 3


async def test_tokens_patch_route_with_password(app):
    response = await app.patch(
        '/tokens',
        data=dumps({
            "data": {
                "dominion":"default",
                "tenant":"default",
                "username":"eecheverry",
                "password":"ABC1234"
            }
        }))
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


async def test_registrations_patch_route(app):
    response = await app.patch(
        '/registrations',
        data=dumps({
            "data": {
                "organization":"Knowark",
                "username":"gecheverry",
                "email":"gecheverry@knowark.com",
                "password":"ABC1234",
                "name":"Gabriel Echeverry"}
        }))
    data = await response.text()
    assert response.status == 200


async def test_verifications_patch_route(app):
    token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWN0aXZhdG"
             "lvbiIsInRlbmFudCI6ImRlZmF1bHQiLCJ1aWQiOiIxIn0.KcmGMRHDhIJMv"
             "BdgIk18iMySbFw_JP_YhVtdLAJi8_s")
    response = await app.patch(
        '/verifications',
        data=dumps({
            "data": [{
                "tenant":"default",
                "token":token
            }]
        }))
    data = await response.text()
    assert response.status == 500


async def test_requisitions_patch_route(app):
    response = await app.patch(
        '/requisitions',
        data=dumps({
            "data": [{
                "type":'reset',
                "data":{'email': 'gabeche@gmail.com'}
            }]
        }))
    data = await response.text()
    assert response.status == 200


async def test_registrations_enroll_patch_route(app):
    response = await app.patch(
        '/registrations',
        data=dumps({
            "data": {
                "organization":"Default",
                "username":"masolano",
                "email":"masolano@knowark.com",
                "password":"XYZ1234",
                "name":"Miguel Alexis Solano",
                "enroll":True
            }
        }))
    data = await response.text()
    assert response.status == 200


async def test_users_delete(app, headers) -> None:
    response = await app.delete('/users/1', headers=headers)
    assert response.status == 200

    response = await app.get('/users', headers=headers)
    data_dict = loads(await response.text())['data']

    assert len(data_dict) == 1


async def test_restrictions_delete(app, headers) -> None:
    response = await app.delete('/restrictions/1', headers=headers)
    assert response.status == 200

    response = await app.get('/restrictions', headers=headers)
    data_dict = loads(await response.text())['data']

    assert len(data_dict) == 0

async def test_policies_head(app, headers) -> None:
    response = await app.head('/policies', headers=headers)
    count = response.headers.get('Count')

    assert response.status == 200
    assert int(count) == 1

async def test_policies_get(app, headers) -> None:
    response = await app.get('/policies', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)['data']

    assert len(data_dict) == 1
    assert data_dict[0]['id'] == '1'


async def test_policies_patch_route(app, headers) -> None:
    response = await app.patch(
        '/policies',
        data=dumps({
            "data": [{
                "resource":"Resource name",
                "privilege":"Privilege name",
                "roleId":"1",
                "active":True
            }]
        }),
        headers=headers)

    assert response.status == 200

    response = await app.head('/policies', headers=headers)
    count = response.headers.get('Count')

    assert int(count) == 2

async def test_policies_delete(app, headers) -> None:
    response = await app.delete('/policies/1', headers=headers)
    assert response.status == 200

    response = await app.get('/policies', headers=headers)
    data_dict = loads(await response.text())['data']

    assert len(data_dict) == 0


async def test_users_delete_body(app, headers) -> None:
    entry = {"data": ["1"]}
    response = await app.delete(
        '/users', data=dumps(entry), headers=headers)
    assert response.status == 200

    response = await app.get('/users', headers=headers)
    data_dict = loads(await response.text())

    assert len(data_dict) == 1


async def test_bad_filter_get_route_filter(app, headers) -> None:
    response = await app.get('/users?filter=[[**BAD FILTER**]]',
                             headers=headers)
    content = await response.text()
    data_dict = loads(content)['data']
    assert len(data_dict) == 2


async def test_users_get_route_filter(app, headers) -> None:
    response = await app.get(
        ('/users?filter=["|", ["name", "=", "John"], '
         '["createdAt", "=", 9999999999]]'), headers=headers)
    content = await response.text()
    data_dict = loads(content)['data']
    assert len(data_dict) == 0

async def test_dominions_head(app, headers) -> None:
    response = await app.head('/dominions', headers=headers)
    count = response.headers.get('Count')

    assert response.status == 200
    assert int(count) == 1

async def test_dominions_get(app, headers) -> None:
    response = await app.get('/dominions', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)['data']

    assert len(data_dict) == 1
    assert data_dict[0]['name'] == 'default'


async def test_tenants_get(app, headers) -> None:
    response = await app.get('/tenants', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)

    assert len(data_dict['data']) == 1
    assert data_dict['data'][0]['slug'] == 'default'


async def test_dominions_not_implemented_put(app, headers) -> None:
    response = await app.put(
        '/dominions',
        data=dumps(dict(
            name="cloudapp"
        )), headers=headers)
    content = await response.text()
    assert response.status == 405


async def test_dominions_not_implemented_delete(app, headers) -> None:
    response = await app.delete('/dominions/platform', headers=headers)
    content = await response.text()
    assert response.status == 500

async def test_ranking_head(app, headers) -> None:
    response = await app.head('/rankings', headers=headers)
    count = response.headers.get('Count')

    assert response.status == 200
    assert int(count) == 1

async def test_ranking_get(app, headers) -> None:
    response = await app.get('/rankings', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)['data']

    assert len(data_dict) == 1
    assert data_dict[0]['id'] == '1'


async def test_ranking_patch_route(app, headers) -> None:
    response = await app.patch(
        '/rankings',
        data=dumps({
            "data":[{
                "userId":"1",
                "roleId":"1"
            }]
        }),
        headers=headers)

    assert response.status == 200

    response = await app.head('/rankings', headers=headers)
    count = response.headers.get('Count')

    assert int(count) == 1

async def test_ranking_delete(app, headers) -> None:
    response = await app.delete('/rankings/1', headers=headers)
    assert response.status == 200

    response = await app.get('/rankings', headers=headers)
    data_dict = loads(await response.text())['data']

    assert len(data_dict) == 0

async def test_restriction_head(app, headers) -> None:
    response = await app.head('/restrictions', headers=headers)
    count = response.headers.get('Count')

    assert response.status == 200
    assert int(count) == 1

async def test_restriction_get(app, headers) -> None:
    response = await app.get('/restrictions', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)['data']

    assert len(data_dict) == 1
    assert data_dict[0]['id'] == '1'


async def test_restrictions_patch_route(app, headers) -> None:
    response = await app.patch(
        '/restrictions',
        data=dumps({
            "data":[{
                "policyId":"1",
                "name":"Restriction name",
                "sequence":"1",
                "target":"Target name",
                "domain":"domain"
            }]
        }),
        headers=headers)

    assert response.status == 200

    response = await app.head('/restrictions', headers=headers)
    count = response.headers.get('Count')

    assert int(count) == 2

async def test_restriction_delete(app, headers) -> None:
    response = await app.delete('/restrictions/1', headers=headers)
    assert response.status == 200

    response = await app.get('/restrictions', headers=headers)
    data_dict = loads(await response.text())['data']

    assert len(data_dict) == 0

async def test_role_head(app, headers) -> None:
    response = await app.head('/roles', headers=headers)
    count = response.headers.get('Count')

    assert response.status == 200
    assert int(count) == 1

async def test_role_get(app, headers) -> None:
    response = await app.get('/roles', headers=headers)
    content = await response.text()
    assert response.status == 200

    data_dict = loads(content)['data']

    assert len(data_dict) == 1
    assert data_dict[0]['id'] == '1'


async def test_role_patch_route(app, headers) -> None:
    response = await app.patch(
        '/roles',
        data=dumps({
            "data":[{
                "name": "admin",
                "dominionId": "1",
                "description": "Systems Administrator"
            }]
        }),
        headers=headers)

    assert response.status == 200

    response = await app.head('/roles', headers=headers)
    count = response.headers.get('Count')

    assert int(count) == 2

async def test_roles_delete(app, headers) -> None:
    response = await app.delete('/roles/1', headers=headers)
    assert response.status == 200

    response = await app.get('/roles', headers=headers)
    data_dict = loads(await response.text())['data']

    assert len(data_dict) == 0
