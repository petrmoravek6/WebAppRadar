from abc import ABC, abstractmethod
from typing import Iterable

from src.latest_version.cycle_info import VersionCycleInfo


class IFetchMethod(ABC):
    @abstractmethod
    def get_all_releases(self) -> Iterable[VersionCycleInfo]:
        pass
