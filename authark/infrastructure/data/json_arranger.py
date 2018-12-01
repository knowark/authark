import json
from pathlib import Path
from typing import List


class JsonArranger:

    @staticmethod
    def make_json(filename: str, collections: List[str]) -> None:

        parent_path = Path(filename).parent
        parent_path.mkdir(parents=True, exist_ok=True)
        filepath = Path(filename)
        filepath.touch()

        with filepath.open('r') as f:
            content = f.read() or "{}"
            data = json.loads(content)

            for collection in collections:
                if collection not in data:
                    data[collection] = {}

            with filepath.open('w') as f:
                json.dump(data, f)
