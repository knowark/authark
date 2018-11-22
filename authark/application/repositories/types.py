from typing import List, Union, Tuple, TypeVar

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = List[Union[str, TermTuple]]

T = TypeVar('T')
