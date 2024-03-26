from abc import ABC, abstractmethod
from typing import Iterable


class IWebServerScanner(ABC):
    """
    Interface used for searching for active web servers
    """
    @abstractmethod
    def discover(self, hosts: Iterable[str]) -> Iterable[str]:
        """
        Searches all given IP addresses or subnets for running web server.

        :param str hosts: iterable object of IP addresses and subnets to search for
        :return: all unique IP addresses from given input where web server is running
        """
        pass
