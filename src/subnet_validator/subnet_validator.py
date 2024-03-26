from abc import ABC, abstractmethod


class ISubnetValidator(ABC):
    @abstractmethod
    def is_ip_in_subnet(self, ip_address: str, subnet: str) -> bool:
        pass