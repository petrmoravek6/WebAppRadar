from abc import ABC, abstractmethod
from typing import Iterable


class IVhostDiscoverer(ABC):
    @abstractmethod
    def get_virtual_hosts(self, ip: str) -> Iterable[str]:
        pass
