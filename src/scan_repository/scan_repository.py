from abc import ABC, abstractmethod
from typing import Collection

from src.web_app_radar import HostnameInfo


class IScanRepository(ABC):
    @abstractmethod
    def read_all(self) -> Collection[HostnameInfo]:
        pass

    @abstractmethod
    def read(self) -> HostnameInfo:
        pass

    @abstractmethod
    def create(self, scan_result: HostnameInfo) -> None:
        pass
