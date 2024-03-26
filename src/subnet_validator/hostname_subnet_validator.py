from abc import ABC, abstractmethod


class IHostnameSubnetValidator(ABC):
    @abstractmethod
    def is_hostname_in_subnet(self, hostname: str, subnet: str) -> bool:
        pass
