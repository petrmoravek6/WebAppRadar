from typing import NamedTuple, Optional
from src.latest_version.full_web_app_info import FullWebAppInfo


class HostnameInfo(NamedTuple):
    hostname: str
    full_web_app_info: Optional[FullWebAppInfo]