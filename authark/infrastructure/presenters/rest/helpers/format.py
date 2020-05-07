import re
from json import loads, JSONDecodeError
from typing import List, Dict, Any


def parse_domain(filter: str) -> List[Any]:
    domain: List[Any] = []
    try:
        domain = loads(filter or "")
    except JSONDecodeError:
        return domain

    for condition in domain:
        word = camel_to_snake(condition[0])
        condition[0] = word

    return domain


def camel_to_snake(value: str) -> str:
    value = re.sub(r"[\-\.\s]", '_', str(value))
    return (value[0].lower() +
            re.sub(r"[A-Z]", lambda matched: '_' +
                   matched.group(0).lower(), value[1:]))
