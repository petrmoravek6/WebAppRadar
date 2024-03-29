from abc import ABC, abstractmethod
from typing import Iterable, Dict


class IOpenPortScanner(ABC):
    """
    Interface used for scanning hosts for open ports
    """
    @abstractmethod
    def get_open_ports(self, hosts: Iterable[str], ports: Iterable[int]) -> Dict[str, Dict[str, bool]]:
        """
        Scans given hosts and checks their open ports. It only checks ports from the parameter.
        :param hosts: An iterable object of hosts to scan
        :param ports: An iterable object of ports to search for when looking for open ports
        :return: A dictionary where keys are hosts and values are open ports. The key is only present if the host is up.
        Open ports are in format of a dictionary where keys are the given ports from method parameter and values are
        booleans signalizing whether the port is open.
        """
        pass
