from pytest import fixture, raises
from json import dump
from authark.infrastructure.data import load_json, LoadingError


@fixture(scope='session')
def filepath(tmpdir_factory):
    filepath = str(tmpdir_factory.mktemp(
        'data_dir').join('data.json'))

    data = {'key_1': 'value_1'}

    with open(filepath, 'w') as f:
        dump(data, f)

    return str(filepath)


def test_load_json(filepath):
    result = load_json(filepath)
    assert result == {'key_1': 'value_1'}


def test_load_json_not_exists(filepath):
    with raises(LoadingError):
        load_json('missing.json')
