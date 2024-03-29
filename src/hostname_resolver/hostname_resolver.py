from abc import ABC, abstractmethod


class IHostnameResolver(ABC):
    @abstractmethod
    def get_ip(self, hostname: str) -> str:
        """
        Converts a hostname or IP address to an IP address according to its CNAME record

        :return: IP address corresponding to given input
        :param hostname: hostname (or IP address) as string
        """
        pass
