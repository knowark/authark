# from json import dump, loads
# from pathlib import Path
# from pytest import fixture, raises
# from authark.application.models import Entity
# from authark.application.utilities import (
#     QueryParser, EntityNotFoundError, StandardTenantProvider, Tenant)
# from authark.application.repositories import Repository
# from authark.infrastructure.data import JsonRepository


# class DummyEntity:
#     def __init__(self, id: str = '', field_1: str = '') -> None:
#         self.id = id
#         self.field_1 = field_1


# def test_json_repository_implementation() -> None:
#     assert issubclass(JsonRepository, Repository)


# @fixture
# def json_repository(tmp_path) -> JsonRepository:
#     item_dict = {
#         "1": vars(DummyEntity('1', 'value_1')),
#         "2": vars(DummyEntity('2', 'value_2')),
#         "3": vars(DummyEntity('3', 'value_3'))
#     }
#     print("tmp path        ", tmp_path)
#     tenant_directory = tmp_path / "default"
#     tenant_directory.mkdir(parents=True)
#     collection = 'dummies'
#     print("tenant_directory   ", tenant_directory)
#     file_path = str(tenant_directory / f'{collection}.json')

#     with open(file_path, 'w') as f:
#         dump({collection: item_dict}, f, indent=2)

#     parser = QueryParser()
#     tenant_provider = StandardTenantProvider()
#     tenant_provider.setup(Tenant(name="Origin"))

#     json_repository = JsonRepository(
#         data_path=str(tmp_path),
#         parser=parser,
#         tenant_provider=tenant_provider,
#         collection=collection,
#         item_class=DummyEntity)

#     return json_repository


# async def test_json_repository_add(json_repository):
#     item = {
#         "4": {'id': '4',
#               'field_4': 'value_4'}
#     }
#     await json_repository.add(item)

#     file_path = Path(json_repository.data_path) / "default/dummies.json"
#     with file_path.open() as f:
#         data = loads(f.read())
#         items = data.get("dummies")

#         item_dict = items.get('5')

#         assert item_dict.get('field_1') == item.field_1


# # async def test_json_repository_add_no_id(json_repository) -> None:
# #     item = DummyEntity(field_1='value_5')
# #     item = await json_repository.add(item)

# #     file_path = str(json_repository._file_path)
# #     with open(file_path) as f:
# #         data = loads(f.read())
# #         items = data.get("dummies")
# #         for key in items:
# #             assert len(key) > 0


# # async def test_json_repository_add_update(json_repository) -> None:
# #     id = '3'
# #     updated_entity = DummyEntity(id=uid, field_1="New Value")

# #     is_updated = await json_repository.add(updated_entity)

# #     file_path = str(json_repository._file_path)
# #     with open(file_path) as f:
# #         data = loads(f.read())
# #         items = data.get("dummies")

# #         assert len(items) == 3
# #         assert is_updated is True
# #         assert "New Value" in items['1']['field_1']


# # async def test_json_repository_search(json_repository):
# #     id = '4'
# #     domain = [('field_1', '=', "value_3")]
# #     items = await json_repository.search(domain)

# #     assert len(items) == 1
# #     for item in items:
# #         assert item.id == id
# #         assert item.field_1 == "value_3"


# # async def test_sql_repository_search_in_ids(sql_repository):  # copied instark
# #     id_2 = '1'
# #     id_3 = '2'

# #     domain = [('id', 'in', [id_2, id_3])]
# #     items = await sql_repository.search(domain)

# #     assert len(items) == 2
# #     assert items[0].id == id_2
# #     assert items[1].id == id_3


# # async def test_json_repository_search_all(json_repository):
# #     items = await json_repository.search([])
# #     assert len(items) == 3


# # async def test_json_repository_search_limit(json_repository):
# #     items = await json_repository.search([], limit=2)
# #     assert len(items) == 2


# # async def test_json_repository_search_limit_zero(json_repository):
# #     items = await json_repository.search([], limit=0)
# #     assert len(items) == 0


# # async def test_json_repository_search_offset(json_repository):
# #     items = await json_repository.search([], offset=2)
# #     assert len(items) == 1


# # async def test_json_repository_remove(json_repository):
# #     file_path = str(json_repository._file_path)
# #     with open(file_path) as f:
# #         data = loads(f.read())
# #         items_dict = data.get("dummies")
# #         item_dict = items_dict.get('2')

# #     item = DummyEntity(**item_dict)
# #     deleted = await json_repository.remove(item)

# #     with open(file_path) as f:
# #         data = loads(f.read())
# #         items_dict = data.get("dummies")

# #     assert deleted is True
# #     assert len(items_dict) == 2
# #     assert "2" not in items_dict.keys()


# # async def test_json_repository_remove_empty(json_repository):
# #     result = await json_repository.remove([])

# #     assert result is False


# # async def test_json_repository_bulk_add(json_repository):
# #     item_4 = DummyEntity(
# #         id='4',
# #         field_1='value_4'
# #     )
# #     item_5 = DummyEntity(
# #         id='5',
# #         field_1='value_5')

# #     items = [item_4, item_5]

# #     items = await json_repository.add(items)

# #     file_path = Path(json_repository.data_path) / "default/dummies.json"
# #     with file_path.open() as f:
# #         data = loads(f.read())
# #         items = data.get("dummies")

# #         item_dict_4 = items.get('4')
# #         item_dict_5 = items.get('5')

# #         assert item_dict_4.get('field_1') == item_4.field_1
# #         assert item_dict_5.get('field_1') == item_5.field_1


# # async def test_json_repository_bulk_add_update(json_repository):
# #     item_1 = DummyEntity(
# #         id='1',
# #         field_1='value_1'
# #     )
# #     item_3 = DummyEntity(
# #         id='3',
# #         field_1='value_3')

# #     items = [item_1, item_3]

# #     items = await json_repository.add(items)

# #     file_path = Path(json_repository.data_path) / "default/dummies.json"
# #     with file_path.open() as f:
# #         data = loads(f.read())
# #         items = data.get("dummies")

# #         item_dict_1 = items.get('1')
# #         item_dict_2 = items.get('2')
# #         item_dict_3 = items.get('3')

# #         assert result is True
# #         assert len(items) == 3
# #         assert item_dict_1.get('field_1') == 'updated_value_1'
# #         assert item_dict_2.get('field_1') == 'value_2'
# #         assert item_dict_3.get('field_1') == 'updated_value_3'


# # async def test_json_repository_bulk_delete(json_repository):
# #     item_1 = DummyEntity(
# #         id='1',
# #         field_1='value_1'
# #     )
# #     item_3 = DummyEntity(
# #         id='3',
# #         field_1='value_3')

# #     items = [item_1, item_3]

# #     items = await json_repository.remove(items)

# #     file_path = Path(json_repository.data_path) / "default/dummies.json"
# #     with file_path.open() as f:
# #         data = loads(f.read())
# #         items = data.get("dummies")

# #         item_dict_2 = items.get('2')

# #         assert result is True
# #         assert len(items) == 1
# #         assert item_dict_2.get('field_1') == 'value_2'
