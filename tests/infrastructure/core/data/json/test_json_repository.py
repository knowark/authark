from json import dumps, loads
from pytest import fixture
from authark.application.domain.models import Entity
from authark.application.domain.common import (
    QueryParser, StandardTenantProvider, Tenant)
from authark.application.domain.repositories import Repository
from authark.infrastructure.core.data import JsonRepository


class DummyEntity(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.field_1 = attributes.get('field_1', '')


def test_json_repository_implementation() -> None:
    assert issubclass(JsonRepository, Repository)


@fixture
def json_repository(tmp_path) -> JsonRepository[DummyEntity]:
    item_dict = {
        "1": vars(DummyEntity(id='1', field_1='value_1')),
        "2": vars(DummyEntity(id='2', field_1='value_2')),
        "3": vars(DummyEntity(id='3', field_1='value_3'))
    }

    tenant_directory = tmp_path / "origin"
    tenant_directory.mkdir(parents=True)
    collection = 'dummies'

    file_path = str(tenant_directory / f'{collection}.json')

    with open(file_path, 'w') as f:
        data = dumps({collection: item_dict})
        f.write(data)

    parser = QueryParser()
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(name="Origin"))

    json_repository = JsonRepository(
        data_path=str(tmp_path),
        parser=parser,
        tenant_provider=tenant_provider,
        collection=collection,
        item_class=DummyEntity)

    return json_repository


async def test_json_repository_add(json_repository):
    item = DummyEntity(id='5', field_1='value_5')

    await json_repository.add(item)

    file_path = json_repository.file_path
    with open(file_path) as f:
        data = loads(f.read())
        items = data.get("dummies")

        item_dict = items.get('5')

        assert item_dict.get('field_1') == item.field_1


async def test_json_repository_add_no_id(json_repository) -> None:
    item = DummyEntity(field_1='value_5')
    item = await json_repository.add(item)

    file_path = json_repository.file_path
    with open(file_path) as f:
        data = loads(f.read())
        items = data.get("dummies")
        for key in items:
            assert len(key) > 0


async def test_json_repository_add_update(json_repository) -> None:
    update = DummyEntity(id='1', field_1='New Value')

    await json_repository.add(update)

    file_path = json_repository.file_path
    with open(file_path) as f:
        data = loads(f.read())
        items = data.get("dummies")

        assert len(items) == 3
        assert "New Value" in items['1']['field_1']


async def test_json_repository_add_non_existent_file(
        tmp_path, json_repository):
    json_repository.data_path = str(tmp_path / '.non_existent_file')
    item = DummyEntity(**{'id': '6', 'field_1': 'value_6'})
    items = await json_repository.add(item)
    assert len(items) == 1


async def test_json_repository_search(json_repository):
    domain = [('field_1', '=', "value_3")]
    items = await json_repository.search(domain)

    assert len(items) == 1
    for item in items:
        assert item.id == '3'
        assert item.field_1 == "value_3"


async def test_json_repository_search_all(json_repository):
    items = await json_repository.search([])
    assert len(items) == 3


async def test_json_repository_search_limit(json_repository):
    domain = []
    items = await json_repository.search(domain, limit=2)
    assert len(items) == 2


async def test_json_repository_search_limit_zero(json_repository):
    items = await json_repository.search([], limit=0)
    assert len(items) == 0


async def test_json_repository_search_offset(json_repository):
    domain = []
    items = await json_repository.search(domain, offset=2)

    assert len(items) == 1


async def test_json_repository_search_limit_and_offset_none(json_repository):
    items = await json_repository.search([], limit=None, offset=None)
    assert len(items) == 3


async def test_json_repository_search_non_existent_file(
        tmp_path, json_repository):
    json_repository.data_path = str(tmp_path / '.non_existent_file')
    items = await json_repository.search([])
    assert len(items) == 0


async def test_json_repository_remove(json_repository):
    file_path = json_repository.file_path

    with open(file_path) as f:
        data = loads(f.read())
        items_dict = data.get("dummies")
        item_dict = items_dict.get('2')

    assert len(items_dict) == 3

    item = DummyEntity(**item_dict)
    deleted = await json_repository.remove(item)

    with open(file_path) as f:
        data = loads(f.read())
        items_dict = data.get("dummies")

    assert deleted is True
    assert len(items_dict) == 2
    assert "2" not in items_dict.keys()


async def test_json_repository_remove_false(json_repository):
    file_path = json_repository.file_path

    item = DummyEntity(**{'id': '5', 'field_1': 'MISSING'})
    deleted = await json_repository.remove(item)

    with open(file_path) as f:
        data = loads(f.read())
        items_dict = data.get("dummies")

    assert deleted is False
    assert len(items_dict) == 3


async def test_json_repository_remove_non_existent_file(
        tmp_path, json_repository):
    json_repository.data_path = str(tmp_path / '.non_existent_remove')
    item = DummyEntity(**{'id': '6', 'field_1': 'MISSING'})
    deleted = await json_repository.remove(item)
    assert deleted is False


async def test_json_repository_count(json_repository):
    count = await json_repository.count()
    assert count == 3


async def test_json_repository_count(json_repository):
    json_repository.data_path = '/tmp/.non_existent_count'
    count = await json_repository.count()
    assert count == 0


async def test_json_repository_count_domain(json_repository):
    domain = [('id', '=', "1")]
    count = await json_repository.count(domain)
    assert count == 1
