from typing import Sequence, List, Dict, Union, Tuple, MutableMapping, Any


TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = Sequence[Union[str, TermTuple]]

DataDict = MutableMapping[str, Any]

RecordList = List[DataDict]


Attribute = Union[int, str, float]

Attributes = Dict[str, Attribute]
