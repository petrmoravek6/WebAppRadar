from abc import ABC, abstractmethod
from typing import Optional

from src.web_app_determiner.web_app_info import WebAppInfo


class IWebAppDetectionMethod(ABC):
    """Interface used for web app detection. This interface allows you to detect name and current version of a web app running on given hostname"""
    @abstractmethod
    def inspect_host(self, host: str) -> Optional[WebAppInfo]:
        """Gets web app information (name and version) of a web app running on given hostname. If no web app can be detected, returns None"""
        pass
