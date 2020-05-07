from json import loads, dumps


async def test_root(app) -> None:
    response = await app.get('/')

    content = await response.text()

    assert response.status == 200
    assert 'Authark' in content


# async def test_root_api(app) -> None:
#     response = await app.get('/?api')
#     data = await response.text()
#     api = loads(data)

#     assert 'openapi' in api
#     assert api['info']['title'] == 'Authark'


# async def test_processes_head(app, headers) -> None:
#     response = await app.head('/processes', headers=headers)
#     count = response.headers.get('Total-Count')

#     assert int(count) == 3


# async def test_processes_get_unauthorized(app) -> None:
#     response = await app.get('/processes')
#     content = await response.text()

#     assert response.status == 401
#     data_dict = loads(content)
#     assert 'error' in data_dict


# async def test_processes_get(app, headers) -> None:
#     response = await app.get('/processes', headers=headers)
#     content = await response.text()
#     assert response.status == 200

#     data_dict = loads(content)

#     assert len(data_dict) == 3
#     assert data_dict[1]['id'] == '002'


# async def test_processes_put(app, headers) -> None:
#     process_data = dumps([{
#         'id': '07506ce5-edd7-4eab-af9c-4e555bc8e098',
#         'name': 'Sales Progress Notification'}])

#     response = await app.put('/processes', data=process_data,
#                              headers=headers)
#     assert response.status == 200

#     response = await app.head('/processes', headers=headers)
#     count = response.headers.get('Total-Count')

#     assert int(count) == 4


# async def test_processes_delete(app, headers) -> None:
#     response = await app.delete('/processes/001', headers=headers)
#     assert response.status == 204

#     response = await app.get('/processes', headers=headers)
#     data_dict = loads(await response.text())

#     assert len(data_dict) == 2


# async def test_processes_delete_body(app, headers) -> None:
#     ids = dumps(["001"])
#     response = await app.delete(
#         '/processes', data=ids, headers=headers)
#     assert response.status == 204

#     response = await app.get('/processes', headers=headers)
#     data_dict = loads(await response.text())

#     assert len(data_dict) == 2


# async def test_processes_get_route_filter(app, headers) -> None:
#     response = await app.get(
#         '/processes?filter=[["name", "=", "Datawarehouse Sync"]]',
#         headers=headers)
#     content = await response.text()
#     data_dict = loads(content)
#     assert len(data_dict) == 1


# async def test_bad_filter_get_route_filter(app, headers) -> None:
#     response = await app.get('/processes?filter=[[**BAD FILTER**]]',
#                              headers=headers)
#     content = await response.text()
#     data_dict = loads(content)
#     assert len(data_dict) == 3


# async def test_triggers_get(app, headers) -> None:
#     response = await app.get('/triggers', headers=headers)
#     content = await response.text()
#     assert response.status == 200

#     data_dict = loads(content)

#     assert len(data_dict) == 1
#     assert data_dict[0]['processId'] == '001'


# async def test_triggers_get_route_filter(app, headers) -> None:
#     response = await app.get(
#         '/triggers?filter=[["processId", "=", "001"]]',
#         headers=headers)
#     content = await response.text()
#     data_dict = loads(content)
#     assert len(data_dict) == 1
#     assert data_dict[0]['processId'] == '001'
