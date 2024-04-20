from abc import ABC, abstractmethod
from typing import Iterable, Collection


class IVhostNetScanner(ABC):
    """
    Interface used for fetching server names from given subnet
    """
    @abstractmethod
    def get_all_vhosts(self, subnets: Iterable[str]) -> Collection[str]:
        """
        Returns a list of all vhosts in the given subnets
        :param subnets: a list of network subnets either in '192.168.60.0/20' or '192.168.60.0' (IP alone) format
        :return: list of all server names bind to the given subnet
        """
        pass
