from abc import ABC, abstractmethod


class IHostnameResolver(ABC):
    @abstractmethod
    def resolve_ip(self, hostname: str) -> str:
        pass
