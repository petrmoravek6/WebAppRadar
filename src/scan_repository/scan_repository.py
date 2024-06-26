from abc import ABC, abstractmethod
from typing import Iterable, Collection, List
from src.hostname_info import HostnameInfo


class IScanRepository(ABC):
    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def get_detail(self, _id: int):
        pass

    @abstractmethod
    def create(self, _id: str, status: str, subnets: Iterable[str], web_app_results: Collection[HostnameInfo]):
        pass
