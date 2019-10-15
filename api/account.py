from typing import NamedTuple
from mapping import GUID


class Account(NamedTuple):
    number: int = 0
    guid: GUID = GUID("")
