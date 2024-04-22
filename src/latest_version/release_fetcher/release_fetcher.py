from functools import partial
from typing import Iterable, Dict
from src.latest_version.cycle_info import VersionCycleInfo
import logging

logger = logging.getLogger(__name__)


class ReleaseFetcher:
    def __init__(self, methods: Dict[str, partial]):
        self.methods = methods

    def fetch_web_app_cycle_info(self, web_app_name: str) -> Iterable[VersionCycleInfo]:
        if web_app_name not in self.methods:
            logger.info(f"Latest release version information could not be fetched for {web_app_name} because it is "
                        f"not supported.")
            return tuple()
        return self.methods[web_app_name]()
