from typing import Dict, List
from pytest import fixture, raises
from inspect import signature
from authark.application.utilities import (
    ExpressionParser, EntityNotFoundError, StandardTenantProvider, Tenant)
from authark.application.repositories import (
    Repository, MemoryRepository)


class DummyEntity:
    def __init__(self, id: str="", field_1: str="") -> None:
        self.id = id
        self.field_1 = field_1


def test_memory_repository_implementation() -> None:
    assert issubclass(MemoryRepository, Repository)


@fixture
def memory_repository() -> MemoryRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    parser = ExpressionParser()
    repository = MemoryRepository[DummyEntity](parser, tenant_provider)
    repository.load({"default": {}})
    return repository


@fixture
def filled_memory_repository(memory_repository) -> MemoryRepository:
    data_dict = {
        "default": {
            "1": DummyEntity('1', 'value_1'),
            "2": DummyEntity('2', 'value_2'),
            "3": DummyEntity('3', 'value_3')
        }
    }
    memory_repository.load(data_dict)
    return memory_repository


def test_memory_repository_tenant_provider(filled_memory_repository) -> None:
    assert filled_memory_repository.tenant_provider is not None


def test_memory_repository_get(filled_memory_repository) -> None:
    item = filled_memory_repository.get("1")

    assert item and item.field_1 == "value_1"


def test_memory_repository_get_missing(filled_memory_repository) -> None:
    with raises(EntityNotFoundError):
        filled_memory_repository.get("999999999")


def test_memory_repository_add(memory_repository) -> None:
    item = DummyEntity("1", "value_1")

    is_saved = memory_repository.add(item)

    assert len(memory_repository.data['default']) == 1
    assert is_saved
    assert "1" in memory_repository.data['default'].keys()
    assert item in memory_repository.data['default'].values()


def test_memory_repository_update(memory_repository) -> None:
    memory_repository.data = {
        "default": {
            '1': DummyEntity("1", "value_1")
        }
    }

    updated_entity = DummyEntity("1", "New Value")

    is_updated = memory_repository.update(updated_entity)

    items = memory_repository.data['default']
    assert len(items) == 1
    assert is_updated is True
    assert "1" in items.keys()
    assert updated_entity in items.values()
    assert "New Value" in items['1'].field_1


def test_memory_repository_update_false(memory_repository):
    memory_repository.data = {
        "default": {
            '1': DummyEntity("1", "value_1")
        }
    }

    missing_entity = DummyEntity("99", "New Value")

    is_updated = memory_repository.update(missing_entity)

    items = memory_repository.data['default']
    assert len(items) == 1
    assert is_updated is False


def test_memory_repository_add_no_id(memory_repository) -> None:
    item = DummyEntity(field_1="value_1")

    is_saved = memory_repository.add(item)

    items = memory_repository.data['default']
    assert len(items) == 1
    assert is_saved
    assert len(list(items.keys())[0]) > 0
    assert item in items.values()


def test_memory_repository_search(filled_memory_repository):
    domain = [('field_1', '=', "value_3")]

    items = filled_memory_repository.search(domain)

    assert len(items) == 1
    for item in items:
        assert item.id == '3'
        assert item.field_1 == "value_3"


def test_memory_repository_search_all(filled_memory_repository):
    items = filled_memory_repository.search([])

    assert len(items) == 3


def test_memory_repository_search_limit(filled_memory_repository):
    items = filled_memory_repository.search([], limit=2)

    assert len(items) == 2


def test_memory_repository_search_limit_zero(filled_memory_repository):
    items = filled_memory_repository.search([], limit=0)

    assert len(items) == 3


def test_memory_repository_search_offset(filled_memory_repository):
    items = filled_memory_repository.search([], offset=2)

    assert len(items) == 1


def test_memory_repository_remove_true(filled_memory_repository):
    item = filled_memory_repository.data['default']["2"]
    deleted = filled_memory_repository.remove(item)

    items = filled_memory_repository.data['default']
    assert deleted is True
    assert len(items) == 2
    assert "2" not in items


def test_memory_repository_remove_false(filled_memory_repository):
    item = DummyEntity(**{'id': '6', 'field_1': 'MISSING'})
    deleted = filled_memory_repository.remove(item)

    items = filled_memory_repository.data['default']
    assert deleted is False
    assert len(items) == 3


def test_memory_repository_bulk_add(memory_repository):
    item_1 = DummyEntity("1", "value_1")
    item_2 = DummyEntity("2", "value_2")

    items = memory_repository.add([item_1, item_2])

    assert len(memory_repository.data['default']) == 2
    assert "1" in memory_repository.data['default'].keys()
    assert "2" in memory_repository.data['default'].keys()


def test_memory_repository_bulk_update(filled_memory_repository):
    item_1 = DummyEntity("1", "updated_value_1")
    item_2 = DummyEntity("3", "updated_value_3")

    result = filled_memory_repository.update([item_1, item_2])

    items = filled_memory_repository.data['default']
    assert result is True
    assert len(items) == 3
    assert items['1'].field_1 == 'updated_value_1'
    assert items['2'].field_1 == 'value_2'
    assert items['3'].field_1 == 'updated_value_3'


def test_memory_repository_bulk_remove(filled_memory_repository):
    item_1 = DummyEntity("1", "value_1")
    item_2 = DummyEntity("3", "value_3")

    result = filled_memory_repository.remove([item_1, item_2])

    items = filled_memory_repository.data['default']
    assert result is True
    assert len(items) == 1
    assert items['2'].field_1 == 'value_2'
