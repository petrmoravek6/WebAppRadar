from datetime import date
from typing import NamedTuple, Optional


class VersionCycleInfo(NamedTuple):
    cycle: str
    latest: str
    eol: Optional[bool] = None
    eol_date: Optional[date] = None
