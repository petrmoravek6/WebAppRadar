from abc import ABC, abstractmethod
from typing import Iterable


class IVhostDiscoverer(ABC):
    """
    Interface used for getting all virtual hosts server names from the host's web server
    """
    @abstractmethod
    def get_virtual_hosts(self, host: str) -> Iterable[str]:
        """
        Gets all server names from the host's web server
        :param host: ip address or hostname
        :return: list of virtual hosts
        """
        pass
