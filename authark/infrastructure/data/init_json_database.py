import os
from json import dump

JSON_DATABASE_SCHEMA = {
    'users': {}
}


def init_json_database(path: str) -> bool:
    if os.path.exists(path):
        return False
    with open(path, 'w') as f:
        dump(JSON_DATABASE_SCHEMA, f)
    return True
