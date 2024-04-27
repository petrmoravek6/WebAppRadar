from abc import ABC, abstractmethod


class IHostnameSubnetValidator(ABC):
    """
    Interface used for checking if a resolved hostname falls within specific subnet
    """
    @abstractmethod
    def is_hostname_in_subnet(self, hostname: str, subnet: str) -> bool:
        """
        The hostname is resolved by reverse DNS lookup and the IP is than checked to fall within given subnet.
        :param hostname: hostname to be resolved and checked
        :param subnet: subnet either in '192.168.60.0/20' or '192.168.60.0' (ip alone) format
        :return: True if hostname is in given subnet
        """
        pass
