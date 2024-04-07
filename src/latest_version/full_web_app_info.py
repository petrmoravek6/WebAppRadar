from datetime import date
from typing import NamedTuple, Optional


class FullWebAppInfo(NamedTuple):
    name: str
    version: Optional[str] = None
    latest_version: Optional[str] = None
    latest_cycle_version: Optional[str] = None
    eol: Optional[bool] = None
    eol_date: Optional[date] = None
