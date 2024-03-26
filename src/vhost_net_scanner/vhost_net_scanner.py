from abc import ABC, abstractmethod
from typing import Iterable


class IVhostNetScanner(ABC):
    @abstractmethod
    def get_all_vhosts(self, subnet: str) -> Iterable[str]:
        pass
