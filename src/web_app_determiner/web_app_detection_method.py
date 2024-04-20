from abc import ABC, abstractmethod
from typing import Optional

from src.web_app_determiner.web_app_info import WebAppInfo


class IWebAppDetectionMethod(ABC):
    """Interface used for web app detection"""
    @abstractmethod
    def inspect_host(self, host: str) -> Optional[WebAppInfo]:
        pass
