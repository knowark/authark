from typing import Sequence, List, Union, Tuple, TypeVar

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = Sequence[Union[str, TermTuple]]

T = TypeVar('T')