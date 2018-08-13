from typing import List, Dict, Union, Tuple, Any

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = List[Union[str, TermTuple]]

TokenString = str

UserDict = Dict[str, Any]
