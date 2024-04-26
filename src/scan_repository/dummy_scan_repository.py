from typing import Iterable, Collection, List

from src.scan_repository.scan_repository import IScanRepository
from src.hostname_info import HostnameInfo


class DummyScanRepository(IScanRepository):
    def get_all(self) -> List:
        return []

    def get_detail(self, _id: int):
        return None

    def create(self, _id: str, status: str, subnets: Iterable[str], web_app_results: Collection[HostnameInfo]):
        return
