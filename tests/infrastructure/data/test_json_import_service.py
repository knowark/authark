# from json import dump, loads
# from pathlib import Path
# from pytest import fixture, raises
# from pprint import pprint
# from authark.application.models import User, Credential, Role, Dominion
# from authark.application.services import MemoryHashService
# from authark.infrastructure.data import JsonImportService


# @fixture
# def file(tmp_path):
#     users_dict = {
#         "1": {'id': '1', 'external_source': 'External Source',
#               'external_id': '1', 'username': 'jjalvarezl',
#               'email': 'jjalvarez@servagro.com.co',
#               'username': 'Jhon Jairo Alvarez', 'gender': 'M',
#               'password': 'ABC123', 'attributes': ''},
#         "2": {'id': '2', 'external_source': 'External Source',
#               'external_id': '1', 'username': 'eecheverry',
#               'email': 'eecheverry@servagro.com.co',
#               'username': 'Esteban Echeverry', 'gender': 'M',
#               'attributes': ''},
#         "3": {'id': '3', 'external_source': 'External Source',
#               'external_id': '1', 'username': 'masolano',
#               'email': 'masolano@servagro.com.co',
#               'username': 'Alexis Solano', 'gender': 'M',
#               'attributes': '', 'authorization': {
#                   'servagro': {'roles': ['Adiministrator', 'Supervisor']}
#               }}
#     }
#     collection = 'users'

#     file_path = tmp_path / "default"

#     with open(file_path, 'w') as f:
#         dump({collection: users_dict}, f, indent=2)

#     return file_path


# @fixture
# def json_import_service():
#     return JsonImportService(MemoryHashService())


# def test_json_import_service_instantiation(json_import_service):
#     assert isinstance(json_import_service, JsonImportService)


# def test_json_import_service_import_users(json_import_service, file):
#     user_list = json_import_service.import_users(
#         file, "Source changed", "password")

#     assert len(user_list) == 3
#     assert user_list[0][1].value == 'HASHED: ABC123'
#     assert user_list[2][2][0][0].name == 'Adiministrator'
#     assert user_list[2][2][0][1].name == 'servagro'
#     assert user_list[2][2][1][0].name == 'Supervisor'
#     assert user_list[2][2][1][1].name == 'servagro'
