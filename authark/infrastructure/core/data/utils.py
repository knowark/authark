# from pathlib import Path
# from json import load
# from typing import Any


# class LoadingError(Exception):
#     pass


# def load_json(filepath) -> Any:
#     path = Path(filepath)
#     if not path.exists():
#         raise LoadingError("The json file couldn't be loaded.")

#     with path.open() as f:
#         return load(f)
