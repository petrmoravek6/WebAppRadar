from abc import ABC, abstractmethod


class IIPSubnetValidator(ABC):
    """
    Interface used for checking if an IP address falls within specific subnet
    """
    @abstractmethod
    def is_ip_in_subnet(self, ip_address: str, subnet: str) -> bool:
        """
        Checks if an IP address is in given subnet
        :param ip_address: ip address to check
        :param subnet: subnet either in '192.168.60.0/20' or '192.168.60.0' (ip alone) format
        :return: True if IP address is in given subnet
        """
        pass
