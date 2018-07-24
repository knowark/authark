from json import load, dump
from authark.infrastructure.data.init_json_database import init_json_database


def test_init_json_database(tmpdir):
    file_path = str(tmpdir.mkdir("authark").join('authark_data.json'))
    result = init_json_database(file_path)

    data = {}
    with open(file_path) as f:
        data = load(f)

    assert 'users' in data
    assert result is True


def test_init_json_database_existing_file(tmpdir):
    file_path = str(tmpdir.mkdir("authark").join('authark_data.json'))

    with open(file_path, 'w') as f:
        dump({}, f)

    result = init_json_database(file_path)
    assert result is False
