from typing import Dict, List
from time import sleep
from pytest import fixture, raises
from inspect import signature
from authark.application.utilities import (
    QueryParser, EntityNotFoundError, StandardTenantProvider, Tenant)
from authark.application.models import Entity
from authark.application.repositories import (
    Repository, MemoryRepository)


class DummyEntity(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.field_1 = attributes.get('field_1', "")


def test_memory_repository_implementation() -> None:
    assert issubclass(MemoryRepository, Repository)


@fixture
def memory_repository() -> MemoryRepository:
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(id='001', name="Default"))
    parser = QueryParser()
    repository: MemoryRepository = MemoryRepository(
        parser, tenant_provider)
    repository.load({"default": {}})
    return repository


@fixture
def filled_memory_repository(memory_repository) -> MemoryRepository:
    data_dict = {
        "default": {
            "1": DummyEntity(id='1', field_1='value_1'),
            "2": DummyEntity(id='2', field_1='value_2'),
            "3": DummyEntity(id='3', field_1='value_3')
        }
    }
    memory_repository.load(data_dict)
    return memory_repository


def test_memory_repository_tenant_provider(filled_memory_repository) -> None:
    assert filled_memory_repository.tenant_provider is not None


# def test_memory_repository_get(filled_memory_repository) -> None:
#     item = filled_memory_repository.get("1")

#     assert item and item.field_1 == "value_1"


# def test_memory_repository_get_missing(filled_memory_repository) -> None:
#     with raises(EntityNotFoundError):
#         filled_memory_repository.get("999999999")


async def test_memory_repository_add(memory_repository) -> None:
    item = DummyEntity("1", "value_1")

    is_saved = await memory_repository.add(item)

    assert len(memory_repository.data['default']) == 1
    assert is_saved
    assert "1" in memory_repository.data['default'].keys()
    assert item in memory_repository.data['default'].values()


async def test_memory_repository_add_update(memory_repository) -> None:
    created_entity = DummyEntity(id="1", field_1="value_1")
    created_entity, *_ = await memory_repository.add(created_entity)

    sleep(1)

    updated_entity = DummyEntity(id="1", field_1="New Value")
    updated_entity, *_ = await memory_repository.add(updated_entity)

    assert created_entity.created_at == updated_entity.created_at

    items = memory_repository.data['default']
    assert len(items) == 1
    assert "1" in items.keys()
    assert updated_entity in items.values()
    assert "New Value" in items['1'].field_1


# def test_memory_repository_update(memory_repository) -> None:
#     memory_repository.data = {
#         "default": {
#             '1': DummyEntity("1", "value_1")
#         }
#     }

#     updated_entity = DummyEntity("1", "New Value")

#     is_updated = memory_repository.update(updated_entity)

#     items = memory_repository.data['default']
#     assert len(items) == 1
#     assert is_updated is True
#     assert "1" in items.keys()
#     assert updated_entity in items.values()
#     assert "New Value" in items['1'].field_1


# def test_memory_repository_update_false(memory_repository):
#     memory_repository.data = {
#         "default": {
#             '1': DummyEntity("1", "value_1")
#         }
#     }

#     missing_entity = DummyEntity("99", "New Value")

#     is_updated = memory_repository.update(missing_entity)

#     items = memory_repository.data['default']
#     assert len(items) == 1
#     assert is_updated is False


async def test_memory_repository_add_no_id(memory_repository) -> None:
    item = DummyEntity(field_1="value_1")

    is_saved = await memory_repository.add(item)

    items = memory_repository.data['default']
    assert len(items) == 1
    assert is_saved
    assert len(list(items.keys())[0]) > 0
    assert item in items.values()


async def test_memory_repository_search(filled_memory_repository):
    domain = [('field_1', '=', "value_3")]

    items = await filled_memory_repository.search(domain)

    assert len(items) == 1
    for item in items:
        assert item.id == '3'
        assert item.field_1 == "value_3"


async def test_memory_repository_search_all(filled_memory_repository):
    items = await filled_memory_repository.search([])

    assert len(items) == 3


async def test_memory_repository_search_limit(filled_memory_repository):
    items = await filled_memory_repository.search([], limit=2)

    assert len(items) == 2


async def test_memory_repository_search_limit_zero(filled_memory_repository):
    items = await filled_memory_repository.search([], limit=0)

    assert len(items) == 0


async def test_memory_repository_search_offset(filled_memory_repository):
    items = await filled_memory_repository.search([], offset=2)

    assert len(items) == 1


async def test_memory_repository_count(filled_memory_repository):
    count = await filled_memory_repository.count()

    assert count == 3


async def test_memory_repository_count_domain(filled_memory_repository):
    domain = [('field_1', '=', "value_3")]
    count = await filled_memory_repository.count(domain)

    assert count == 1


async def test_memory_repository_remove_true(filled_memory_repository):
    item = filled_memory_repository.data['default']["2"]
    deleted = await filled_memory_repository.remove(item)

    items = filled_memory_repository.data['default']
    assert deleted is True
    assert len(items) == 2
    assert "2" not in items


async def test_memory_repository_remove_false(filled_memory_repository):
    item = DummyEntity(**{'id': '6', 'field_1': 'MISSING'})
    deleted = await filled_memory_repository.remove(item)

    items = filled_memory_repository.data['default']
    assert deleted is False
    assert len(items) == 3


async def test_memory_repository_remove_idempotent(filled_memory_repository):
    existing_item = item = filled_memory_repository.data['default']["2"]
    missing_item = DummyEntity(**{'id': '6', 'field_1': 'MISSING'})

    items = filled_memory_repository.data['default']

    deleted = await filled_memory_repository.remove(
        [existing_item, missing_item])

    assert deleted is True
    assert len(items) == 2

    deleted = await filled_memory_repository.remove(
        [existing_item, missing_item])

    assert deleted is False
    assert len(items) == 2


async def test_memory_repository_bulk_add(memory_repository):
    item_1 = DummyEntity("1", "value_1")
    item_2 = DummyEntity("2", "value_2")

    items = await memory_repository.add([item_1, item_2])

    assert len(memory_repository.data['default']) == 2
    assert "1" in memory_repository.data['default'].keys()
    assert "2" in memory_repository.data['default'].keys()


async def test_memory_repository_bulk_update(filled_memory_repository):
    item_1 = DummyEntity("1", "updated_value_1")
    item_2 = DummyEntity("3", "updated_value_3")

    result = await filled_memory_repository.update([item_1, item_2])

    items = filled_memory_repository.data['default']
    assert result is True
    assert len(items) == 3
    assert items['1'].field_1 == 'updated_value_1'
    assert items['2'].field_1 == 'value_2'
    assert items['3'].field_1 == 'updated_value_3'


async def test_memory_repository_bulk_remove(filled_memory_repository):
    item_1 = DummyEntity("1", "value_1")
    item_2 = DummyEntity("3", "value_3")

    result = await filled_memory_repository.remove([item_1, item_2])

    items = filled_memory_repository.data['default']
    assert result is True
    assert len(items) == 1
    assert items['2'].field_1 == 'value_2'
