from abc import ABC, abstractmethod


class IHostnameResolver(ABC):
    @abstractmethod
    def resolve(self, ip: str) -> str:
        pass
