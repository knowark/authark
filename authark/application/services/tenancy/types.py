from typing import List, Union, Tuple, Sequence

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = Sequence[Union[str, TermTuple]]
