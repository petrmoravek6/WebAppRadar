from datetime import date
from typing import NamedTuple, Optional


class CycleInfo(NamedTuple):
    cycle: str
    latest: str
    eol: Optional[bool]
    eol_date: Optional[date]
