from abc import ABC, abstractmethod
from typing import Iterable, Dict


class OpenPortScanner(ABC):
    @abstractmethod
    def get_open_ports(self, hosts: Iterable[str], ports: Iterable[int]) -> Dict[str, Dict[str, bool]]:
        pass
