from datetime import date
from typing import NamedTuple, Optional


class VersionComparison(NamedTuple):
    latest_version: Optional[str]
    latest_cycle_version: Optional[str]
    eol: Optional[bool]
    eol_date: Optional[date]
