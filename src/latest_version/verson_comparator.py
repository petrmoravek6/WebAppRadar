from abc import ABC, abstractmethod
from typing import Iterable
from src.latest_version.cycle_info import CycleInfo
from src.latest_version.version_comparison import VersionComparison

class IVersionComparator(ABC):
    @abstractmethod
    def get_version_comparison(self, curr_version: str, ver_cycles: Iterable[CycleInfo]) -> VersionComparison:
        pass
