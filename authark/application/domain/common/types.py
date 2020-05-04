from typing import Sequence, List, Dict, Union, Tuple, Any, MutableMapping


TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = Sequence[Union[str, TermTuple]]

DataDict = MutableMapping[str, Any]

RecordList = List[DataDict]

ExtendedRankingDict = Dict[str, Any]

ExtendedRankingDictList = List[ExtendedRankingDict]

TokenString = str

TokensDict = Dict[str, Any]
