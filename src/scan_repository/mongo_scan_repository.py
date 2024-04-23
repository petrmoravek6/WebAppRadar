import os
from typing import Collection
from pymongo import MongoClient
from src.scan_repository.scan_repository import IScanRepository
from src.web_app_radar import HostnameInfo


class MongoScanRepository(IScanRepository):
    def __init__(self, connection_string: str):
        client = MongoClient(connection_string)
        self.db = client.web_app_radar

    def read_all(self) -> Collection[HostnameInfo]:
        pass

    def read(self) -> HostnameInfo:
        pass

    def create(self, scan_result: HostnameInfo) -> None:
        self.db.results.insert_one(scan_result)
