from abc import ABC, abstractmethod
from typing import Iterable


class IVhostNetScanner(ABC):
    """
    Interface used for fetching server names from given subnet
    """
    @abstractmethod
    def get_all_vhosts(self, subnet: str) -> Iterable[str]:
        """
        Returns a list of all vhosts in the given subnet
        :param subnet: subnet either in '192.168.60.0/20' or '192.168.60.0' (ip alone) format
        :return: list of all server names bind to the given subnet
        """
        pass
