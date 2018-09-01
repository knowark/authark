import os
from json import dump

JSON_DATABASE_SCHEMA = {  # type: ignore
    'users': {},
    'credentials': {}
}


def init_json_database(path: str) -> bool:
    if os.path.exists(path):
        return False
    with open(path, 'w') as f:
        dump(JSON_DATABASE_SCHEMA, f)  # type: ignore
    return True
