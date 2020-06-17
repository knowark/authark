from asyncio import sleep
from pytest import fixture, raises
from authark.application.domain.common import (
    QueryParser, StandardTenantProvider, Tenant)
from authark.application.domain.models import Entity
from authark.application.domain.repositories import (
    Repository, MemoryRepository)


class Dummy(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.field_1 = attributes.get('field_1', "")


class Child(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.dummy_id = attributes.get('dummy_id', "")


def test_memory_repository_implementation() -> None:
    assert issubclass(MemoryRepository, Repository)


@fixture
def memory_repository() -> MemoryRepository[Dummy]:
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(id='001', name="Default"))
    parser = QueryParser()

    class DummyMemoryRepository(MemoryRepository[Dummy]):
        model = Dummy

    repository = DummyMemoryRepository(parser, tenant_provider)

    repository.load({"default": {}})
    return repository


@fixture
def filled_memory_repository(memory_repository) -> MemoryRepository[Dummy]:
    data_dict = {
        "default": {
            "1": Dummy(id='1', field_1='value_1'),
            "2": Dummy(id='2', field_1='value_2'),
            "3": Dummy(id='3', field_1='value_3')
        }
    }
    memory_repository.load(data_dict)
    return memory_repository


@fixture
def child_memory_repository() -> MemoryRepository[Child]:
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(id='001', name="Default"))
    parser = QueryParser()

    class ChildMemoryRepository(MemoryRepository[Child]):
        model = Child

    repository = ChildMemoryRepository(parser, tenant_provider)
    repository.load({"default": {}})
    return repository


@fixture
def filled_child_memory_repository(
        child_memory_repository) -> MemoryRepository[Child]:
    data_dict = {
        "default": {
            "1": Child(id='1', dummy_id='1'),
            "2": Child(id='2', dummy_id='1'),
            "3": Child(id='3', dummy_id='2')
        }
    }
    child_memory_repository.load(data_dict)
    return child_memory_repository


def test_memory_repository_model(memory_repository) -> None:
    assert memory_repository.model is Dummy


def test_memory_repository_not_implemented_model(memory_repository) -> None:
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(id='001', name="Default"))
    parser = QueryParser()
    repository = MemoryRepository(parser, tenant_provider)
    with raises(NotImplementedError):
        repository.model


def test_memory_repository_tenant_provider(filled_memory_repository) -> None:
    assert filled_memory_repository.tenant_provider is not None


async def test_memory_repository_search_limit(filled_memory_repository):
    items = await filled_memory_repository.search([], limit=2)

    assert len(items) == 2


async def test_memory_repository_search_limit_none(filled_memory_repository):
    items = await filled_memory_repository.search([], limit=None, offset=None)

    assert len(items) == 3


async def test_memory_repository_search_offset(filled_memory_repository):
    items = await filled_memory_repository.search([], offset=2)

    assert len(items) == 1


async def test_memory_repository_add(memory_repository) -> None:
    item = Dummy(id="1", field_1="value_1")

    is_saved = await memory_repository.add(item)

    assert len(memory_repository.data['default']) == 1
    assert is_saved
    assert "1" in memory_repository.data['default'].keys()
    assert item in memory_repository.data['default'].values()


async def test_memory_repository_add_update(memory_repository) -> None:
    created_entity = Dummy(id="1", field_1="value_1")
    created_entity, *_ = await memory_repository.add(created_entity)

    await sleep(1)

    updated_entity = Dummy(id="1", field_1="New Value")
    updated_entity, *_ = await memory_repository.add(updated_entity)

    assert created_entity.created_at == updated_entity.created_at

    items = memory_repository.data['default']
    assert len(items) == 1
    assert "1" in items.keys()
    assert updated_entity in items.values()
    assert "New Value" in items['1'].field_1


async def test_memory_repository_add_no_id(memory_repository) -> None:
    item = Dummy(field_1="value_1")

    is_saved = await memory_repository.add(item)

    items = memory_repository.data['default']
    assert len(items) == 1
    assert is_saved
    assert len(list(items.keys())[0]) > 0
    assert item in items.values()


async def test_memory_repository_add_multiple(memory_repository):
    items = [
        Dummy(field_1="value_1"),
        Dummy(field_1="value_2")
    ]

    returned_items = await memory_repository.add(items)

    items = memory_repository.data['default']
    assert len(returned_items) == 2
    assert returned_items[0].field_1 == 'value_1'
    assert returned_items[1].field_1 == 'value_2'


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


async def test_memory_repository_search_join_one_to_many(
        filled_memory_repository, filled_child_memory_repository):

    for parent, children in await filled_memory_repository.search(
            [('id', '=', '1')], join=filled_child_memory_repository):

        assert isinstance(parent, Dummy)
        assert all(isinstance(child, Child) for child in children)
        assert len(children) == 2


async def test_memory_repository_search_join_many_to_one(
        filled_memory_repository, filled_child_memory_repository):

    for element, siblings in await filled_child_memory_repository.search(
            [('id', '=', '1')], join=filled_memory_repository,
            link=filled_memory_repository):

        assert isinstance(element, Child)
        assert len(siblings) == 1
        assert isinstance(next(iter(siblings)), Dummy)


async def test_memory_repository_remove_true(filled_memory_repository):
    item = filled_memory_repository.data['default']["2"]
    deleted = await filled_memory_repository.remove(item)

    items = filled_memory_repository.data['default']
    assert deleted is True
    assert len(items) == 2
    assert "2" not in items


async def test_memory_repository_remove_false(filled_memory_repository):
    item = Dummy(**{'id': '6', 'field_1': 'MISSING'})
    deleted = await filled_memory_repository.remove(item)

    items = filled_memory_repository.data['default']
    assert deleted is False
    assert len(items) == 3


async def test_memory_repository_remove_idempotent(filled_memory_repository):
    existing_item = item = filled_memory_repository.data['default']["2"]
    missing_item = Dummy(**{'id': '6', 'field_1': 'MISSING'})

    items = filled_memory_repository.data['default']

    deleted = await filled_memory_repository.remove(
        [existing_item, missing_item])

    assert deleted is True
    assert len(items) == 2

    deleted = await filled_memory_repository.remove(
        [existing_item, missing_item])

    assert deleted is False
    assert len(items) == 2


async def test_memory_repository_count(filled_memory_repository):
    count = await filled_memory_repository.count()

    assert count == 3


async def test_memory_repository_count_domain(filled_memory_repository):
    domain = [('field_1', '=', "value_3")]
    count = await filled_memory_repository.count(domain)

    assert count == 1
