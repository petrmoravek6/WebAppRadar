from abc import ABC, abstractmethod


class IIPSubnetValidator(ABC):
    @abstractmethod
    def is_ip_in_subnet(self, ip_address: str, subnet: str) -> bool:
        pass
